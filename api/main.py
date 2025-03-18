from fastapi import FastAPI
from typing import Optional, Dict, Any
from temporalio.client import Client
from temporalio.exceptions import TemporalError
from temporalio.api.enums.v1 import WorkflowExecutionStatus
from fastapi import HTTPException
from dotenv import load_dotenv
import asyncio
import os
import logging
import subprocess
import sys
import time
import threading
import os.path

from workflows.agent_goal_workflow import AgentGoalWorkflow
from workflows.agent_selector import AgentSelectorWorkflow
from models.data_types import CombinedInput, AgentGoalWorkflowParams
from tools.goal_registry import goal_match_train_invoice, goal_event_flight_invoice, music_creation_goal, json_array_creation_goal, unified_agent_goal
from fastapi.middleware.cors import CORSMiddleware
from shared.config import get_temporal_client, TEMPORAL_TASK_QUEUE

app = FastAPI()
temporal_client: Optional[Client] = None
temporal_available = False

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # React dev server default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add a global flag to track if we've tried to start the worker
worker_start_attempted = False

def get_agent_goal(goal_name: str = None):
    """Get the agent goal based on name or environment variable."""
    if goal_name is None:
        goal_name = os.getenv("AGENT_GOAL", "unified_agent_goal")
    
    goals = {
        "goal_match_train_invoice": goal_match_train_invoice,
        "goal_event_flight_invoice": goal_event_flight_invoice,
        "music_creation_goal": music_creation_goal,
        "json_array_creation_goal": json_array_creation_goal,
        "unified_agent_goal": unified_agent_goal,
    }
    return goals.get(goal_name, unified_agent_goal)


async def select_agent_goal(conversation_history: str) -> str:
    """
    Uses the agent selector workflow to determine the most appropriate 
    agent goal based on the conversation history.
    
    Args:
        conversation_history: The conversation history
        
    Returns:
        The name of the selected agent goal
    """
    global temporal_client, temporal_available
    if temporal_client is None or not temporal_available:
        return "unified_agent_goal"  # Default if Temporal not available
    
    try:
        # Execute the agent selector workflow
        selector_result = await temporal_client.execute_workflow(
            AgentSelectorWorkflow.run,
            conversation_history,
            id=f"agent-selector-{asyncio.current_task().get_name()}",
            task_queue=TEMPORAL_TASK_QUEUE,
        )
        
        return selector_result.get("selected_goal", "unified_agent_goal")
    except Exception as e:
        logger.error(f"Error in select_agent_goal: {e}")
        return "unified_agent_goal"  # Default on error


def start_temporal_worker_process():
    """Start the Temporal worker process in a separate thread."""
    global worker_start_attempted
    
    if worker_start_attempted:
        logger.info("Worker start already attempted, won't try again")
        return
    
    worker_start_attempted = True
    
    def run_worker():
        try:
            logger.info("Attempting to start Temporal worker...")
            
            # Check if the worker script exists
            worker_script = "scripts/run_worker.py"
            if not os.path.exists(worker_script):
                logger.error(f"Worker script not found: {worker_script}")
                return
            
            # Use Python executable from sys.executable to ensure we use the same environment
            cmd = [sys.executable, worker_script]
            
            # Start the worker process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Log the start attempt
            logger.info(f"Started Temporal worker process with PID: {process.pid}")
            
            # Wait a few seconds to see if it crashes immediately
            time.sleep(3)
            
            if process.poll() is not None:
                # Process exited already
                stdout, stderr = process.communicate()
                logger.error(f"Worker process exited immediately with code {process.returncode}")
                logger.error(f"STDOUT: {stdout}")
                logger.error(f"STDERR: {stderr}")
            else:
                logger.info("Worker process started successfully and is still running")
        
        except Exception as e:
            logger.error(f"Error starting worker process: {e}")
    
    # Start in a daemon thread so it doesn't prevent the server from shutting down
    worker_thread = threading.Thread(target=run_worker, daemon=True)
    worker_thread.start()


@app.on_event("startup")
async def startup_event():
    global temporal_client, temporal_available
    try:
        temporal_client = await get_temporal_client()
        temporal_available = True
        logger.info("Successfully connected to Temporal service")
        
        # Try to verify a deeper connection by checking if worker is available
        try:
            # Try to describe a random workflow to see if we get a "not found" response
            await temporal_client.get_workflow_handle("test-worker-connectivity").describe()
        except TemporalError as e:
            if "not found" in str(e).lower():
                # This is the expected error if the service is working
                logger.info("Temporal service verified working properly")
            else:
                # Some other error - maybe worker is not running?
                logger.warning(f"Temporal service connected but workers may not be running: {e}")
                # Try to start the worker
                start_temporal_worker_process()
                
    except Exception as e:
        logger.error(f"Failed to connect to Temporal service: {e}")
        temporal_available = False
        # Set client to None to ensure we don't try to use an invalid client
        temporal_client = None
        
        # If we failed to connect, try to start the worker
        # as that might be the issue
        start_temporal_worker_process()


@app.get("/")
def root():
    global temporal_available
    return {
        "message": "Temporal AI Agent!",
        "temporal_available": temporal_available
    }


@app.get("/get-temporal-status")
async def get_temporal_status():
    """Returns the current status of the Temporal connection."""
    global temporal_available, temporal_client
    
    if not temporal_client:
        try:
            # Try to create a new client
            logger.info("No existing client, attempting to create a new one")
            temporal_client = await get_temporal_client()
            temporal_available = True
            return {"available": True}
        except Exception as e:
            logger.error(f"Failed to create new Temporal client: {e}")
            temporal_available = False
            return {"available": False, "error": str(e)}
    
    try:
        # First check if the client is responding
        await temporal_client.get_system_info()
        
        # Then try to check if a workflow can be created
        try:
            # Try to describe a workflow (even if it doesn't exist)
            # This tests a deeper level of connectivity
            await temporal_client.get_workflow_handle("test-workflow-health-check").describe()
        except TemporalError as e:
            # If we get "not found", that's actually good - it means we could communicate 
            # with the server, even though the workflow doesn't exist
            if "not found" in str(e).lower():
                logger.info("Temporal connectivity check succeeded")
                temporal_available = True
                return {"available": True}
            else:
                # Any other error might indicate a deeper issue
                logger.warn(f"Temporal connectivity check found issue: {e}")
        
        # If we get here, basic operations succeeded
        temporal_available = True
        return {"available": True}
    except Exception as e:
        logger.error(f"Error checking Temporal status: {e}")
        
        # Try to recreate the client
        try:
            logger.info("Attempting to refresh Temporal client connection")
            temporal_client = await get_temporal_client()
            temporal_available = True
            return {"available": True, "refreshed": True}
        except Exception as refresh_error:
            logger.error(f"Failed to refresh Temporal client: {refresh_error}")
            temporal_available = False
            return {"available": False, "error": str(e)}


@app.get("/tool-data")
async def get_tool_data():
    """Calls the workflow's 'get_tool_data' query."""
    global temporal_client, temporal_available
    
    if not temporal_client or not temporal_available:
        return {"error": "Temporal service unavailable", "status": "error"}
    
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
    global temporal_client, temporal_available
    
    if not temporal_client or not temporal_available:
        return {"messages": []}  # Return empty messages if Temporal is down
    
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
            return {"messages": []}

        # Set a timeout for the query
        try:
            conversation_history = await asyncio.wait_for(
                handle.query("get_conversation_history"),
                timeout=5,  # Timeout after 5 seconds
            )
            return conversation_history
        except asyncio.TimeoutError:
            logger.error("Temporal query timed out (worker may be unavailable)")
            return {"messages": []}  # Return empty messages on timeout

    except TemporalError as e:
        error_message = str(e)
        logger.error(f"Temporal error: {error_message}")
        
        # Return empty messages instead of raising exceptions
        return {"messages": []}


@app.post("/send-prompt")
async def send_prompt(prompt: str):
    global temporal_client, temporal_available
    
    if not temporal_client or not temporal_available:
        return {"message": "Cannot send prompt: Temporal service unavailable", "error": True}
    
    try:
        # Create combined input with goal from environment
        combined_input = CombinedInput(
            tool_params=AgentGoalWorkflowParams(None, None),
            agent_goal=get_agent_goal(),
        )

        workflow_id = "agent-workflow"

        # Start (or signal) the workflow
        await temporal_client.start_workflow(
            AgentGoalWorkflow.run,
            combined_input,
            id=workflow_id,
            task_queue=TEMPORAL_TASK_QUEUE,
            start_signal="user_prompt",
            start_signal_args=[prompt],
        )

        return {"message": f"Prompt '{prompt}' sent to workflow {workflow_id}."}
    except Exception as e:
        logger.error(f"Error sending prompt: {e}")
        return {"message": f"Error sending prompt: {str(e)}", "error": True}


@app.post("/confirm")
async def send_confirm():
    """Sends a 'confirm' signal to the workflow."""
    global temporal_client, temporal_available
    
    if not temporal_client or not temporal_available:
        return {"message": "Cannot confirm: Temporal service unavailable", "error": True}
    
    try:
        workflow_id = "agent-workflow"
        handle = temporal_client.get_workflow_handle(workflow_id)
        await handle.signal("confirm")
        return {"message": "Confirm signal sent."}
    except Exception as e:
        logger.error(f"Error in confirm: {e}")
        return {"message": f"Error confirming: {str(e)}", "error": True}


@app.post("/end-chat")
async def end_chat():
    """Sends a 'end_chat' signal to the workflow."""
    global temporal_client, temporal_available
    
    if not temporal_client or not temporal_available:
        return {"message": "No active chat to end (Temporal unavailable)", "status": "ok"}
    
    try:
        workflow_id = "agent-workflow"
        handle = temporal_client.get_workflow_handle(workflow_id)
        await handle.signal("end_chat")
        return {"message": "End chat signal sent."}
    except TemporalError as e:
        logger.info(f"No workflow found to end: {e}")
        # This is actually expected sometimes, so return success
        return {"message": "No active chat to end"}
    except Exception as e:
        logger.error(f"Error ending chat: {e}")
        return {"message": f"Error ending chat: {str(e)}", "error": True}


@app.post("/start-workflow")
async def start_workflow():
    global temporal_client, temporal_available
    
    if not temporal_client or not temporal_available:
        return {"message": "Cannot start workflow: Temporal service unavailable", "error": True}
    
    try:
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
    except Exception as e:
        logger.error(f"Error starting workflow: {e}")
        return {"message": f"Error starting workflow: {str(e)}", "error": True}


@app.post("/run-tool")
async def run_tool(tool_data: Dict[str, Any]):
    """
    Run a specific tool with provided arguments.
    
    Args:
        tool_data: Dictionary containing tool_name and tool_args
        
    Returns:
        The result from the tool
    """
    try:
        from tools import get_handler
        
        tool_name = tool_data.get("tool_name")
        tool_args = tool_data.get("tool_args", {})
        
        if not tool_name:
            raise HTTPException(status_code=400, detail="Tool name is required")
            
        try:
            # Get the tool handler and run it
            handler = get_handler(tool_name)
            result = handler(tool_args)
            return result
        except ValueError as e:
            # Tool not found or invalid arguments
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            # Other errors during tool execution
            raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/get-workflow-state")
async def get_workflow_state():
    """Calls the workflow's 'get_workflow_state' query to get information about the workflow state."""
    global temporal_client, temporal_available
    
    if not temporal_client or not temporal_available:
        logger.warn("Temporal appears unavailable when getting workflow state - attempting to reconnect")
        try:
            # Try to reconnect
            temporal_client = await get_temporal_client()
            temporal_available = True
            # Continue with the function now that we have a client
        except Exception as e:
            logger.error(f"Failed to reconnect to Temporal: {e}")
            return {"exists": False, "error": "Temporal service unavailable"}
    
    try:
        handle = temporal_client.get_workflow_handle("agent-workflow")

        failed_states = [
            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_TERMINATED,
            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_CANCELED,
            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_FAILED,
        ]

        try:
            description = await handle.describe()
            if description.status in failed_states:
                print("Workflow is in a failed state. Returning error.")
                return {"exists": False, "error": "Workflow is in a failed state"}
        except TemporalError as e:
            # If the workflow doesn't exist, that's an expected error
            if "not found" in str(e).lower():
                return {"exists": False, "not_found": True}
            # For any other error, we try to handle it below
            raise

        # Set a timeout for the query
        try:
            workflow_state = await asyncio.wait_for(
                handle.query("get_workflow_state"),
                timeout=5,  # Timeout after 5 seconds
            )
            # Successfully got the state, reset error flags
            temporal_available = True  
            return workflow_state
        except asyncio.TimeoutError:
            # Return a default response instead of an error
            print("Workflow query timed out. Returning default state.")
            return {"exists": True, "error": "Temporal query timed out (worker may be unavailable)"}
        except TemporalError as e:
            error_message = str(e)
            # Check specifically for the missing query handler error
            if "Query handler for 'get_workflow_state' expected but not found" in error_message:
                print("get_workflow_state query not found. Using fallback approach.")
                # Fallback: Try to get conversation history to determine if workflow exists
                try:
                    conversation = await handle.query("get_conversation_history")
                    message_count = len(conversation.get("messages", []))
                    return {
                        "exists": True,
                        "message_count": message_count,
                        "waiting_for_confirm": False,  # Conservative default
                        "continued_from_previous": False,
                    }
                except Exception:
                    # If even this fails, return minimal info
                    return {"exists": True, "message_count": 0}
            else:
                # For other query errors, return exists=true to prevent unnecessary workflow creation
                return {"exists": True, "error": error_message}

    except TemporalError as e:
        error_message = str(e)
        print(f"Temporal error in get_workflow_state: {error_message}")

        # Check if the error is that the workflow doesn't exist
        if "not found" in error_message.lower():
            return {"exists": False}

        # If worker is down or no poller is available, mark temporal as unavailable 
        if "no poller seen for task queue recently" in error_message:
            temporal_available = False
            return {"exists": False, "error": "Workflow worker unavailable"}
        
        # For other Temporal errors, return a default response
        return {"exists": False, "error": error_message}
