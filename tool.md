# Temporal AI Agent: Tools System Documentation

## Table of Contents
- [Temporal AI Agent: Tools System Documentation](#temporal-ai-agent-tools-system-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Project Structure](#project-structure)
  - [Tool System Overview](#tool-system-overview)
  - [Creating New Tools](#creating-new-tools)
    - [1. Define the Tool](#1-define-the-tool)
    - [2. Implement the Tool](#2-implement-the-tool)
    - [3. Register the Tool](#3-register-the-tool)
    - [4. Add the Tool to a Goal](#4-add-the-tool-to-a-goal)
  - [Temporal Workflow Integration](#temporal-workflow-integration)
    - [Workflow Structure](#workflow-structure)
    - [Tool Activities](#tool-activities)
  - [Backend Implementation](#backend-implementation)
  - [Frontend Integration](#frontend-integration)
  - [Examples: From Temporal to Frontend](#examples-from-temporal-to-frontend)
    - [Example: Music Composition Tool Flow](#example-music-composition-tool-flow)
    - [Example: Tool Confirmation Flow](#example-tool-confirmation-flow)
  - [Prompts and LLM Integration](#prompts-and-llm-integration)

## Introduction

The Temporal AI Agent is a conversational AI system that can perform tasks using specialized tools. The agent runs inside a Temporal workflow, allowing it to maintain state between conversations and interact with various systems through tool activities. This document explains the tool system architecture, how to create new tools, and how the different parts of the system work together.

The agent is designed to collect information towards a goal, using tools along the way. It supports multiple LLM providers (OpenAI, Anthropic, Google, Deepseek, or local Ollama) and can be configured for different goals, each with its own set of tools.

## Project Structure

The project follows a structured architecture with clear separation of concerns:

```
temporal-ai-agent/
├── activities/             # Temporal activities for tool execution
├── api/                    # FastAPI backend endpoints
├── frontend/               # React frontend application
├── models/                 # Data models and type definitions
├── prompts/                # LLM prompt templates
├── tools/                  # Tool implementations
│   ├── data/               # Mock data for tools
│   ├── __init__.py         # Tool registry mapping
│   ├── tool_registry.py    # Tool definitions for LLM
│   ├── goal_registry.py    # Goal configurations
│   └── [tool files].py     # Individual tool implementations
├── workflows/              # Temporal workflows
│   ├── agent_goal_workflow.py  # Main agent workflow
│   └── workflow_helpers.py     # Helper functions
└── scripts/                # Utility scripts
```

## Tool System Overview

In the Temporal AI Agent, tools are functions that the AI can call to perform specific actions. Each tool has:

1. **Definition**: A structured description of what the tool does and what arguments it accepts
2. **Implementation**: The actual code that executes when the tool is called
3. **Registration**: The mechanism that connects the tool definition to its implementation

The system uses a registry pattern to make tools available to the agent:

- `tool_registry.py` contains tool definitions used by the LLM to understand tool capabilities
- `__init__.py` in the tools directory maps tool names to their implementation functions
- `goal_registry.py` groups tools for specific agent goals

## Creating New Tools

Creating a new tool involves several steps:

### 1. Define the Tool

In `tools/tool_registry.py`, define the tool structure:

```python
new_tool = ToolDefinition(
    name="NewTool",
    description="Description of what the tool does and when to use it.",
    arguments=[
        ToolArgument(
            name="arg_name",
            type="string",  # Or other types like "float", "ISO8601", etc.
            description="Description of this argument"
        ),
        # Add more arguments as needed
    ],
)
```

### 2. Implement the Tool

Create a new file in the `tools` directory, for example `tools/new_tool.py`:

```python
def new_tool(args: dict) -> dict:
    """
    Implement the tool functionality here.
    The function should take a dictionary of arguments and return a dictionary result.
    """
    # Extract arguments
    arg_name = args.get("arg_name", "")
    
    # Validation
    if not arg_name:
        return {"error": "Missing required argument"}
    
    # Tool implementation
    result = process_arg(arg_name)
    
    # Return structured response
    return {
        "result": result,
        "status": "success"
    }
```

### 3. Register the Tool

Add your tool to `tools/__init__.py`:

```python
from .new_tool import new_tool

def get_handler(tool_name: str):
    # Add your tool to the existing if statements
    if tool_name == "NewTool":
        return new_tool
    # ...other tools...
```

### 4. Add the Tool to a Goal

In `tools/goal_registry.py`, add your tool to an existing goal or create a new goal:

```python
from .tool_registry import new_tool

new_goal = GoalDefinition(
    name="new_goal",
    description="Description of the goal",
    tools=[
        new_tool,  # Add your new tool here
        # Other tools for this goal
    ]
)
```

## Temporal Workflow Integration

Tools are executed within a Temporal workflow, providing durability, reliability, and state management.

### Workflow Structure

The main workflow (`AgentGoalWorkflow`) in `workflows/agent_goal_workflow.py` manages:

1. Conversation state and history
2. Tool execution
3. User interaction signals
4. LLM invocation

When a tool needs to be executed:

1. The workflow signals a tool activity
2. The activity executes the tool with provided arguments
3. The result is returned to the workflow
4. The workflow updates conversation history and responds to the user

### Tool Activities

Tool activities in `activities/tool_activities.py` provide the interface between the workflow and the actual tool implementations:

```python
@activity.defn
class ToolActivities:
    async def run_tool_from_name(self, tool_name: str, tool_args: dict) -> str:
        """Run a tool by name with the provided arguments."""
        try:
            # Get the tool handler
            handler = get_handler(tool_name)
            
            # Run the tool
            result = handler(tool_args)
            
            return json.dumps(result)
        except Exception as e:
            # Handle errors
            return json.dumps({"error": str(e)})
```

The workflow uses retry policies to handle transient failures and timeouts, ensuring that tools are given adequate time to complete their tasks.

## Backend Implementation

The FastAPI backend (`api/main.py`) serves as the interface between the frontend and the Temporal workflow:

1. **API Endpoints**:
   - `/start-workflow`: Begins a new agent workflow
   - `/send-prompt`: Sends user input to the workflow
   - `/confirm`: Confirms tool execution
   - `/get-conversation-history`: Retrieves conversation history
   - `/tool-data`: Retrieves data about the latest tool execution

2. **Temporal Client Integration**:
   - The API server creates a Temporal client to interact with workflows
   - Signals are used to send user input and commands to the workflow
   - Queries are used to retrieve workflow state without interrupting execution

## Frontend Integration

The React frontend provides a user interface for interacting with the agent:

1. **API Service** (`frontend/src/services/api.js`):
   - Handles communication with the backend API
   - Manages error handling and response processing

2. **Components**:
   - Chat interface for conversation with the agent
   - Tool confirmation UI for reviewing and approving tool execution
   - Result visualization for displaying tool outputs

## Examples: From Temporal to Frontend

### Example: Music Composition Tool Flow

1. **User Request**:
   The user sends a message: "I want to create a jazz composition with piano and saxophone"

2. **Backend Processing**:
   - The message is sent to the workflow via the `/send-prompt` endpoint
   - The workflow passes the message to the LLM for processing

3. **Tool Selection**:
   - The LLM determines that the `CreateMusicComposition` tool is appropriate
   - It formats the arguments: `{"genre": "jazz", "instruments": "piano, saxophone", "mood": "upbeat", "tempo": "moderate"}`

4. **Tool Execution**:
   - The workflow signals the tool activity to run `CreateMusicComposition`
   - The activity calls the tool implementation in `create_music_composition.py`
   - The tool generates a composition and returns metadata

5. **Result Processing**:
   - The workflow receives the tool result and updates conversation history
   - The LLM generates a response to the user incorporating the tool output

6. **Frontend Display**:
   - The frontend polls for conversation updates via `/get-conversation-history`
   - It renders the agent's response and the composition details in the chat interface

### Example: Tool Confirmation Flow

1. **Tool Execution Request**:
   - The LLM suggests using a tool that requires confirmation
   - The workflow updates the latest tool data with the tool name and arguments

2. **Frontend Confirmation**:
   - The frontend fetches the latest tool data via `/tool-data`
   - It displays a confirmation dialog showing the tool and arguments

3. **User Confirmation**:
   - The user reviews and confirms the action
   - The frontend sends a confirmation via the `/confirm` endpoint

4. **Tool Execution**:
   - The workflow receives the confirmation signal
   - It proceeds with tool execution as described earlier

## Prompts and LLM Integration

The agent uses carefully crafted prompts to guide the LLM's behavior:

1. **Prompt Structure**:
   - System message explaining the agent's purpose and available tools
   - Goal description and constraints
   - Tool definitions in a structured format
   - Conversation history

2. **LLM Providers**:
   - The system supports multiple LLM providers (OpenAI, Anthropic, Google, Deepseek, Ollama)
   - Provider selection is configured via environment variables

3. **Output Parsing**:
   - The LLM's response is parsed to extract:
     - Direct responses to the user
     - Tool calls with arguments
     - Next actions (e.g., asking for more information)

Prompts are generated in the `prompts/` directory and include templates for different goals and scenarios.

---

This documentation provides an overview of the Temporal AI Agent's tool system. By following the guidelines for creating new tools, you can extend the agent's capabilities to handle new types of tasks and integrate with additional services.
