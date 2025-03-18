"""
Example Tool Function Implementation

This module demonstrates how to create a tool using the function-based approach with a decorator.
"""
from typing import Dict, Any
import logging
from .base_tool import tool_function

@tool_function
def example_tool_function(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example tool that demonstrates the function-based approach.
    This tool takes a message and returns it with a farewell.
    
    Args:
        args: Dictionary containing the 'message' parameter.
        
    Returns:
        Dictionary containing the farewell and original message.
    """
    # Extract the message from args
    message = args.get("message", "World")
    
    # Log additional information
    logger = logging.getLogger("tool.example_tool_function")
    logger.info(f"Processing message for farewell: {message}")
    
    # Return the result
    return {
        "farewell": f"Goodbye, {message}!",
        "original_message": message,
        "status": "success"
    } 