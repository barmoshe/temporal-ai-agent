from datetime import timedelta
from typing import Dict, Any, Deque
from temporalio import workflow
from temporalio.exceptions import ActivityError
from temporalio.common import RetryPolicy

from models.data_types import ConversationHistory, ToolPromptInput
from prompts.agent_prompt_generators import (
    generate_missing_args_prompt,
    generate_tool_completion_prompt,
)
from shared.config import TEMPORAL_LEGACY_TASK_QUEUE

# Constants from original file
TOOL_ACTIVITY_START_TO_CLOSE_TIMEOUT = timedelta(seconds=12)
TOOL_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT = timedelta(minutes=30)
LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT = timedelta(seconds=20)
LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT = timedelta(minutes=30)


async def handle_tool_execution(
    current_tool: str,
    tool_data: Dict[str, Any],
    tool_results: list,
    add_message_callback: callable,
    prompt_queue: Deque[str],
) -> None:
    """Execute a tool after confirmation and handle its result."""
    workflow.logger.info(f"Confirmed. Proceeding with tool: {current_tool}")

    task_queue = (
        TEMPORAL_LEGACY_TASK_QUEUE
        if current_tool in ["SearchTrains", "BookTrains"]
        else None
    )

    try:
        dynamic_result = await workflow.execute_activity(
            current_tool,
            tool_data["args"],
            task_queue=task_queue,
            schedule_to_close_timeout=TOOL_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
            start_to_close_timeout=TOOL_ACTIVITY_START_TO_CLOSE_TIMEOUT,
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=5), backoff_coefficient=1
            ),
        )
        dynamic_result["tool"] = current_tool
        tool_results.append(dynamic_result)
    except ActivityError as e:
        workflow.logger.error(f"Tool execution failed: {str(e)}")
        dynamic_result = {"error": str(e), "tool": current_tool}

    add_message_callback("tool_result", dynamic_result)
    prompt_queue.append(generate_tool_completion_prompt(current_tool, dynamic_result))


async def handle_missing_args(
    current_tool: str,
    args: Dict[str, Any],
    tool_data: Dict[str, Any],
    prompt_queue: Deque[str],
) -> bool:
    """Check for missing arguments and handle them if found."""
    missing_args = [key for key, value in args.items() if value is None]

    if missing_args:
        prompt_queue.append(
            generate_missing_args_prompt(current_tool, tool_data, missing_args)
        )
        workflow.logger.info(
            f"Missing arguments for tool: {current_tool}: {' '.join(missing_args)}"
        )
        return True
    return False


def format_history(conversation_history: ConversationHistory) -> str:
    """Format the conversation history into a single string."""
    return " ".join(str(msg["response"]) for msg in conversation_history["messages"])


def prompt_with_history(
    conversation_history: ConversationHistory, prompt: str
) -> tuple[str, str]:
    """Generate a context-aware prompt with conversation history."""
    history_string = format_history(conversation_history)
    context_instructions = (
        f"Here is the conversation history: {history_string} "
        "Please add a few sentence response in plain text sentences. "
        "Don't editorialize or add metadata. "
        "Keep the text a plain explanation based on the history."
    )
    return (context_instructions, prompt)


async def continue_as_new_if_needed(
    conversation_history: ConversationHistory,
    prompt_queue: Deque[str],
    agent_goal: Any,
    max_turns: int,
    add_message_callback: callable,
) -> None:
    """Handle workflow continuation if message limit is reached.
    
    This implements Temporal's continue-as-new pattern which allows a workflow to 
    complete its current run and immediately start a new run with the same workflow ID 
    but a fresh event history. This is useful for long-running conversations to prevent
    the history from growing too large.
    """
    if len(conversation_history["messages"]) >= max_turns:
        workflow.logger.info(f"History size reached {max_turns} turns. Preparing to continue as new.")
        
        # Generate a summary of the conversation for the new workflow instance
        try:
            summary_context, summary_prompt = prompt_summary_with_history(conversation_history)
            summary_input = ToolPromptInput(
                prompt=summary_prompt, context_instructions=summary_context
            )
            conversation_summary = await workflow.start_activity_method(
                "ToolActivities.agent_toolPlanner",
                summary_input,
                schedule_to_close_timeout=LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
            )
            workflow.logger.info("Successfully generated conversation summary for continue-as-new")
        except Exception as e:
            # If summarization fails, still continue but with a simpler summary
            workflow.logger.error(f"Failed to generate summary: {str(e)}")
            conversation_summary = {"summary": "Continued conversation from previous session"}
        
        # Add a message to inform the user about the transition
        transition_message = {
            "type": "system",
            "content": "The conversation is continuing in a new session to maintain performance."
        }
        add_message_callback("system", transition_message)
        
        # Add the summary to the conversation history
        add_message_callback("conversation_summary", conversation_summary)
        
        # Create the new parameters for the continued workflow
        workflow.logger.info(f"Continuing as new after {max_turns} turns with {len(prompt_queue)} pending prompts")
        
        # Use continue_as_new to start a fresh workflow with the same ID
        # This is an atomic operation from Temporal's perspective
        workflow.continue_as_new({
            "tool_params": {
                "conversation_summary": conversation_summary,
                "prompt_queue": list(prompt_queue),  # Convert deque to list for serialization
            },
            "agent_goal": agent_goal,
        })
        
        # Note: Any code after continue_as_new is never executed
        # The current workflow run ends and a new one starts immediately


def prompt_summary_with_history(
    conversation_history: ConversationHistory,
) -> tuple[str, str]:
    """Generate a prompt for summarizing the conversation.
    Used only for continue as new of the workflow."""
    # Extract the last 50 messages for a more relevant summary if history is very large
    recent_messages = conversation_history["messages"][-50:] if len(conversation_history["messages"]) > 50 else conversation_history["messages"]
    
    # Format the recent history into a string
    history_string = " ".join(str(msg["response"]) for msg in recent_messages)
    
    context_instructions = (
        f"Here is the recent conversation history between a user and an AI assistant: {history_string}\n\n"
        f"Total conversation length: {len(conversation_history['messages'])} messages."
    )
    
    actual_prompt = (
        "Please produce a concise summary of this conversation that captures the main topics and context. "
        "Include any important details that should be preserved for continuing the conversation. "
        'Put the summary in the format { "summary": "<summary text>", "topics": ["topic1", "topic2"] }'
    )
    return (context_instructions, actual_prompt)
