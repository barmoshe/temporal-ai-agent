"""
Chat Workflow

This module provides a workflow for chat-based interactions using the DefaultChatTool.
The DefaultChatTool serves as the main interface and decides whether to trigger specialized tools.
"""
import logging
import json
from typing import Dict, Any, List, Optional
from tools import get_handler
from tools.chat_utils import format_help_response
from workflow_helpers import run_temporal
from activities.activities import log_activity

logger = logging.getLogger(__name__)

class ChatSession:
    """Manages the state of a chat session."""
    
    def __init__(self, session_id: str):
        """
        Initialize a new chat session.
        
        Args:
            session_id: Unique identifier for the session
        """
        self.session_id = session_id
        self.conversation_history = []
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            role: The role of the message sender ('user' or 'assistant')
            content: The content of the message
        """
        self.conversation_history.append({"role": role, "content": content})
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Returns:
            List of conversation messages
        """
        return self.conversation_history


async def handle_chat_message(session_id: str, message: str) -> Dict[str, Any]:
    """
    Handle a chat message by using the DefaultChatTool to process it.
    
    Args:
        session_id: Unique identifier for the chat session
        message: The user's message
        
    Returns:
        Dictionary containing the response and any actions taken
    """
    # Get or create the chat session
    session = ChatSession(session_id)
    
    # Add the user message to the conversation history
    session.add_message("user", message)
    
    # Log the activity
    await log_activity(
        activity_type="chat_message_received",
        details={"session_id": session_id, "message": message}
    )
    
    # Process the message using the DefaultChatTool
    chat_handler = get_handler("DefaultChatTool")
    chat_result = chat_handler({
        "message": message,
        "conversation_history": session.get_history()
    })
    
    # Check if we should trigger a specialized tool
    if chat_result.get("should_trigger_tool", False):
        tool_name = chat_result.get("suggested_tool")
        tool_args = chat_result.get("suggested_tool_args", {})
        
        logger.info(f"Triggering specialized tool: {tool_name}")
        
        # Log the activity
        await log_activity(
            activity_type="tool_triggered",
            details={"session_id": session_id, "tool": tool_name, "args": tool_args}
        )
        
        # Get the tool handler
        tool_handler = get_handler(tool_name)
        
        # Execute the tool
        tool_result = tool_handler(tool_args)
        
        # Special handling for HelpTool to make responses more conversational
        if tool_name == "HelpTool":
            response = format_help_response(chat_result.get('response', ''), tool_result)
        else:
            # For other tools, combine the chat response with the tool result
            response = f"{chat_result.get('response')} {tool_result.get('result', '')}"
        
        # Add the assistant's response to the conversation history
        session.add_message("assistant", response)
        
        return {
            "response": response,
            "tool_used": tool_name,
            "tool_result": tool_result
        }
    else:
        # No specialized tool was triggered, just use the chat response
        response = chat_result.get("response", "")
        
        # Add the assistant's response to the conversation history
        session.add_message("assistant", response)
        
        # Log the activity
        await log_activity(
            activity_type="chat_response_sent",
            details={"session_id": session_id, "response": response}
        )
        
        return {
            "response": response,
            "tool_used": None,
            "tool_result": None
        }


@run_temporal
async def chat_workflow(session_id: str, message: str) -> Dict[str, Any]:
    """
    Temporal workflow for handling chat-based interactions.
    
    Args:
        session_id: Unique identifier for the chat session
        message: The user's message
        
    Returns:
        Dictionary containing the response and metadata
    """
    logger.info(f"Starting chat workflow for session {session_id}")
    
    # Handle the chat message
    result = await handle_chat_message(session_id, message)
    
    logger.info(f"Chat workflow completed for session {session_id}")
    
    return result 