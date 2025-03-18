"""
Chat Utilities

This module provides utility functions for formatting chat responses
and other common chat-related operations.
"""
from typing import Dict, Any, List


def format_help_response(chat_response: str, help_result: Dict[str, Any]) -> str:
    """
    Format the help tool result into a conversational response.
    
    Args:
        chat_response: The initial chat response
        help_result: The result from the HelpTool
        
    Returns:
        A formatted conversational response
    """
    response_parts = [chat_response]
    
    # Add the help result heading
    if "result" in help_result:
        response_parts.append(help_result["result"])
    
    # Format tool list if present
    if "tools" in help_result:
        response_parts.append("\n\nAvailable tools:")
        for tool in help_result["tools"]:
            response_parts.append(f"• {tool['name']}: {tool['description']}")
    
    # Format specific tool info if present
    if "tool_name" in help_result:
        response_parts.append(f"\n\nTool: {help_result['tool_name']}")
        response_parts.append(f"Description: {help_result['description']}")
        
        # Add arguments
        if "arguments" in help_result:
            response_parts.append("\nArguments:")
            for arg in help_result["arguments"]:
                response_parts.append(f"• {arg['name']} ({arg['type']}): {arg['description']}")
        
        # Add usage example
        if "usage_example" in help_result:
            response_parts.append(f"\nExample: \"{help_result['usage_example']}\"")
    
    # Format system info if present
    if "system_info" in help_result:
        system_info = help_result["system_info"]
        for key, value in system_info.items():
            if key != "name":  # Skip the name as it's usually in the result heading
                response_parts.append(f"\n{value}")
    
    # Format help options if present
    if "options" in help_result:
        response_parts.append("\n\nYou can ask for help in these ways:")
        for option in help_result["options"]:
            response_parts.append(f"• {option}")
    
    # Add any notes
    if "note" in help_result:
        response_parts.append(f"\n{help_result['note']}")
    
    # Add info about asking for more details
    if "info" in help_result:
        response_parts.append(f"\n{help_result['info']}")
    
    return "\n".join(response_parts) 