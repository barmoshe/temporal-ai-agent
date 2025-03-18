from collections import deque
from datetime import timedelta
from typing import Dict, Any, Union, List, Optional, Deque, TypedDict

from temporalio.common import RetryPolicy
from temporalio import workflow

from models.data_types import ConversationHistory, NextStep, ValidationInput
from workflows.workflow_helpers import LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT, \
    LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT
from workflows import workflow_helpers as helpers

with workflow.unsafe.imports_passed_through():
    from activities.tool_activities import ToolActivities
    from prompts.agent_prompt_generators import (
        generate_genai_prompt
    )
    from models.data_types import (
        CombinedInput,
        ToolPromptInput,
    )

# Constants
MAX_TURNS_BEFORE_CONTINUE = 200  # Reduced from 250 to trigger continue-as-new more frequently for testing
WORKFLOW_ID = "agent-workflow"  # Constant workflow ID used by the application

class ToolData(TypedDict, total=False):
    next: NextStep
    tool: str
    args: Dict[str, Any]
    response: str

@workflow.defn
class AgentGoalWorkflow:
    """Workflow that manages tool execution with user confirmation and conversation history."""

    def __init__(self) -> None:
        self.conversation_history: ConversationHistory = {"messages": []}
        self.prompt_queue: Deque[str] = deque()
        self.conversation_summary: Optional[str] = None
        self.chat_ended: bool = False
        self.tool_data: Optional[ToolData] = None
        self.confirm: bool = False
        self.tool_results: List[Dict[str, Any]] = []
        self.continued_from_previous: bool = False

    @workflow.run
    async def run(self, combined_input: CombinedInput) -> str:
        """Main workflow execution method."""
        params = combined_input.tool_params
        agent_goal = combined_input.agent_goal
        workflow.logger.info(f"Starting workflow with ID: {workflow.info().workflow_id}")
        
        # Check if this is a continuation of a previous workflow
        if params and params.conversation_summary:
            self.continued_from_previous = True
            self.add_message("system", {
                "type": "continuation",
                "message": "Continuing conversation from previous session"
            })
            self.add_message("conversation_summary", params.conversation_summary)
            self.conversation_summary = params.conversation_summary
            workflow.logger.info("Continuing workflow with existing conversation summary")

        # Restore the prompt queue if available
        if params and params.prompt_queue:
            if isinstance(params.prompt_queue, list):
                self.prompt_queue.extend(params.prompt_queue)
            else:
                self.prompt_queue.extend([params.prompt_queue])
            workflow.logger.info(f"Restored {len(self.prompt_queue)} items to prompt queue")

        waiting_for_confirm = False
        current_tool = None

        while True:
            # Wait for a signal to arrive (prompt, confirm, or end_chat)
            await workflow.wait_condition(
                lambda: bool(self.prompt_queue) or self.chat_ended or self.confirm
            )

            # Handle end_chat signal (triggered by New Chat button)
            if self.chat_ended:
                workflow.logger.info("Chat ended explicitly by user action.")
                # No continue-as-new here, we just exit with the current history
                return f"{self.conversation_history}"

            # Handle confirm signal
            if self.confirm and waiting_for_confirm and current_tool and self.tool_data:
                self.confirm = False
                waiting_for_confirm = False

                confirmed_tool_data = self.tool_data.copy()
                confirmed_tool_data["next"] = "user_confirmed_tool_run"
                self.add_message("user_confirmed_tool_run", confirmed_tool_data)

                await helpers.handle_tool_execution(
                    current_tool,
                    self.tool_data,
                    self.tool_results,
                    self.add_message,
                    self.prompt_queue
                )
                
                # Check if we need to continue as new after tool execution
                await helpers.continue_as_new_if_needed(
                    self.conversation_history,
                    self.prompt_queue,
                    agent_goal,
                    MAX_TURNS_BEFORE_CONTINUE,
                    self.add_message
                )
                continue

            # Handle user prompt
            if self.prompt_queue:
                prompt = self.prompt_queue.popleft()
                # Don't add starter prompts to the conversation history
                if not prompt.startswith("###"):
                    self.add_message("user", prompt)

                    # Validate the prompt before proceeding
                    validation_input = ValidationInput(
                        prompt=prompt,
                        conversation_history=self.conversation_history,
                        agent_goal=agent_goal,
                    )
                    validation_result = await workflow.execute_activity(
                        ToolActivities.agent_validatePrompt,
                        args=[validation_input],
                        schedule_to_close_timeout=LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                        start_to_close_timeout=LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                        retry_policy=RetryPolicy(
                            initial_interval=timedelta(seconds=5), backoff_coefficient=1
                        ),
                    )

                    if not validation_result.validationResult:
                        workflow.logger.warning(
                            f"Prompt validation failed: {validation_result.validationFailedReason}"
                        )
                        self.add_message(
                            "agent", validation_result.validationFailedReason
                        )
                        continue

                # Proceed with generating the context and prompt
                context_instructions = generate_genai_prompt(
                    agent_goal, self.conversation_history, self.tool_data
                )

                prompt_input = ToolPromptInput(
                    prompt=prompt,
                    context_instructions=context_instructions,
                )

                tool_data = await workflow.execute_activity(
                    ToolActivities.agent_toolPlanner,
                    prompt_input,
                    schedule_to_close_timeout=LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                    start_to_close_timeout=LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                    retry_policy=RetryPolicy(
                        initial_interval=timedelta(seconds=5), backoff_coefficient=1
                    ),
                )
                self.tool_data = tool_data

                next_step = tool_data.get("next")
                current_tool = tool_data.get("tool")

                if next_step == "confirm" and current_tool:
                    args = tool_data.get("args", {})
                    if await helpers.handle_missing_args(current_tool, args, tool_data, self.prompt_queue):
                        continue

                    waiting_for_confirm = True
                    self.confirm = False
                    workflow.logger.info("Waiting for user confirm signal...")

                elif next_step == "done":
                    workflow.logger.info("All steps completed. Exiting workflow.")
                    self.add_message("agent", tool_data)
                    return str(self.conversation_history)

                self.add_message("agent", tool_data)
                
                # Check if we need to continue as new after processing the prompt
                await helpers.continue_as_new_if_needed(
                    self.conversation_history,
                    self.prompt_queue,
                    agent_goal,
                    MAX_TURNS_BEFORE_CONTINUE,
                    self.add_message
                )

    @workflow.signal
    async def user_prompt(self, prompt: str) -> None:
        """Signal handler for receiving user prompts."""
        if self.chat_ended:
            workflow.logger.warn(f"Message dropped due to chat closed: {prompt}")
            return
        workflow.logger.info(f"Received user prompt: {prompt[:50]}...")
        self.prompt_queue.append(prompt)

    @workflow.signal
    async def confirm(self) -> None:
        """Signal handler for user confirmation of tool execution."""
        workflow.logger.info("Received user confirmation")
        self.confirm = True

    @workflow.signal
    async def end_chat(self) -> None:
        """Signal handler for ending the chat session."""
        workflow.logger.info("Received end_chat signal")
        self.chat_ended = True

    @workflow.query
    def get_conversation_history(self) -> ConversationHistory:
        """Query handler to retrieve the full conversation history."""
        return self.conversation_history

    @workflow.query
    def get_workflow_state(self) -> Dict[str, Any]:
        """Query handler to get the current state of the workflow including continuation status."""
        return {
            "message_count": len(self.conversation_history["messages"]),
            "waiting_for_confirm": bool(self.tool_data and self.tool_data.get("next") == "confirm"),
            "continued_from_previous": self.continued_from_previous,
            "max_turns_before_continue": MAX_TURNS_BEFORE_CONTINUE,
        }

    @workflow.query
    def get_summary_from_history(self) -> Optional[str]:
        """Query handler to retrieve the conversation summary if available. 
        Used only for continue as new of the workflow."""
        return self.conversation_summary

    @workflow.query
    def get_latest_tool_data(self) -> Optional[ToolData]:
        """Query handler to retrieve the latest tool data response if available."""
        return self.tool_data

    def add_message(self, actor: str, response: Union[str, Dict[str, Any]]) -> None:
        """Add a message to the conversation history.

        Args:
            actor: The entity that generated the message (e.g., "user", "agent")
            response: The message content, either as a string or structured data
        """
        if isinstance(response, dict):
            response_str = str(response)
            workflow.logger.debug(f"Adding {actor} message: {response_str[:100]}...")
        else:
            workflow.logger.debug(f"Adding {actor} message: {response[:100]}...")

        self.conversation_history["messages"].append(
            {"actor": actor, "response": response}
        )
