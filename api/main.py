from fastapi import FastAPI
from typing import Optional
from temporalio.client import Client
from temporalio.exceptions import TemporalError
from temporalio.api.enums.v1 import WorkflowExecutionStatus
from fastapi import HTTPException
from dotenv import load_dotenv
import asyncio
import os

from workflows.agent_goal_workflow import AgentGoalWorkflow
from models.data_types import CombinedInput, AgentGoalWorkflowParams
from tools.goal_registry import goal_simple_music
from fastapi.middleware.cors import CORSMiddleware
from shared.config import get_temporal_client, TEMPORAL_TASK_QUEUE

app = FastAPI()
temporal_client: Optional[Client] = None

# Load environment variables
load_dotenv()


def get_agent_goal():
    """Get the agent goal from environment variables."""
    goal_name = os.getenv("AGENT_GOAL", "goal_simple_music")
    goals = {
        "goal_simple_music": goal_simple_music,
    }
    return goals.get(goal_name, goal_simple_music)


@app.on_event("startup")
async def startup_event():
    global temporal_client
    temporal_client = await get_temporal_client()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Temporal AI Agent!"}


@app.get("/tool-data")
async def get_tool_data():
    """Calls the workflow's 'get_tool_data' query."""
    try:
        # Get workflow handle
        handle = temporal_client.get_workflow_handle("agent-workflow")

        # Check if the workflow is completed
        workflow_status = await handle.describe()
        if workflow_status.status == 2:
            # Workflow is completed; return an empty response
            return {}

        # Query the workflow
        tool_data = await handle.query("get_tool_data")
        return tool_data
    except TemporalError as e:
        # Workflow not found; return an empty response
        print(e)
        return {}


@app.get("/get-conversation-history")
async def get_conversation_history():
    """Calls the workflow's 'get_conversation_history' query."""
    try:
        handle = temporal_client.get_workflow_handle("agent-workflow")

        failed_states = [
            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_TERMINATED,
            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_CANCELED,
            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_FAILED,
        ]

        description = await handle.describe()
        if description.status in failed_states:
            print("Workflow is in a failed state. Returning empty history.")
            return []

        # Set a timeout for the query
        try:
            conversation_history = await asyncio.wait_for(
                handle.query("get_conversation_history"),
                timeout=5,  # Timeout after 5 seconds
            )
            return conversation_history
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=404,
                detail="Temporal query timed out (worker may be unavailable).",
            )

    except TemporalError as e:
        error_message = str(e)
        print(f"Temporal error: {error_message}")

        # If worker is down or no poller is available, return a 404
        if "no poller seen for task queue recently" in error_message:
            raise HTTPException(
                status_code=404, detail="Workflow worker unavailable or not found."
            )

        # For other Temporal errors, return a 500
        raise HTTPException(
            status_code=500, detail="Internal server error while querying workflow."
        )


@app.post("/send-prompt")
async def send_prompt(prompt: str):
    # Create combined input with goal from environment
    combined_input = CombinedInput(
        tool_params=AgentGoalWorkflowParams(None, None),
        agent_goal=get_agent_goal(),
    )

    workflow_id = "agent-workflow"

    # Check if the prompt is just a number (like "120" for tempo)
    # and if the last message from the agent might be asking for tempo confirmation
    auto_confirm = False
    if prompt.strip().isdigit():
        try:
            # Get conversation history
            handle = temporal_client.get_workflow_handle(workflow_id)
            workflow_info = await handle.describe()
            
            if workflow_info.status == WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_RUNNING:
                # Try to get the last message from history to check if it's asking about tempo/BPM
                try:
                    conversation_history = await handle.query("get_conversation_history")
                    if conversation_history and "messages" in conversation_history:
                        messages = conversation_history["messages"]
                        if messages and len(messages) > 0:
                            last_message = messages[-1]
                            if last_message.get("actor") == "agent" or last_message.get("role") == "assistant":
                                content = last_message.get("content", "").lower()
                                if "tempo" in content and "bpm" in content:
                                    auto_confirm = True
                except Exception as e:
                    print(f"Error checking conversation history: {str(e)}")
        except Exception as e:
            print(f"Error determining if auto-confirm is needed: {str(e)}")

    # Start (or signal) the workflow
    await temporal_client.start_workflow(
        AgentGoalWorkflow.run,
        combined_input,
        id=workflow_id,
        task_queue=TEMPORAL_TASK_QUEUE,
        start_signal="user_prompt",
        start_signal_args=[prompt],
    )

    # If it looks like a tempo response, automatically send a confirm signal
    if auto_confirm:
        try:
            handle = temporal_client.get_workflow_handle(workflow_id)
            await asyncio.sleep(1)  # Small delay to make sure the workflow processes the prompt first
            await handle.signal("confirm")
            return {"message": f"Prompt '{prompt}' sent and automatically confirmed as tempo value."}
        except Exception as e:
            print(f"Auto-confirmation failed: {str(e)}")

    return {"message": f"Prompt '{prompt}' sent to workflow {workflow_id}."}


@app.post("/confirm")
async def send_confirm():
    """Sends a 'confirm' signal to the workflow."""
    workflow_id = "agent-workflow"
    handle = temporal_client.get_workflow_handle(workflow_id)
    await handle.signal("confirm")
    return {"message": "Confirm signal sent."}


@app.post("/end-chat")
async def end_chat():
    """Sends a 'end_chat' signal to the workflow."""
    workflow_id = "agent-workflow"

    try:
        handle = temporal_client.get_workflow_handle(workflow_id)
        await handle.signal("end_chat")
        return {"message": "End chat signal sent."}
    except TemporalError as e:
        print(e)
        # Workflow not found; return an empty response
        return {}


@app.post("/start-workflow")
async def start_workflow():
    # Get the configured goal
    agent_goal = get_agent_goal()

    # Create combined input
    combined_input = CombinedInput(
        tool_params=AgentGoalWorkflowParams(None, None),
        agent_goal=agent_goal,
    )

    workflow_id = "agent-workflow"

    # Start the workflow with the starter prompt from the goal
    await temporal_client.start_workflow(
        AgentGoalWorkflow.run,
        combined_input,
        id=workflow_id,
        task_queue=TEMPORAL_TASK_QUEUE,
        start_signal="user_prompt",
        start_signal_args=["### " + agent_goal.starter_prompt],
    )

    return {
        "message": f"Workflow started with goal's starter prompt: {agent_goal.starter_prompt}."
    }
#POST /api/ai-help 
#implement ai help here 

