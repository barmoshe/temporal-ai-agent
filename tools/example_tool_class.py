"""
Example Tool Class Implementation

This module demonstrates how to create a tool using the class-based approach.
"""
from typing import Dict, Any
from .base_tool import BaseTool

class ExampleTool(BaseTool):
    """
    Example tool that demonstrates the class-based approach.
    This tool takes a message and returns it with a greeting.
    """
    
    def __init__(self):
        """Initialize the example tool."""
        super().__init__(name="ExampleTool")
    
    def _execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement the tool logic.
        
        Args:
            args: Dictionary containing the 'message' parameter.
            
        Returns:
            Dictionary containing the greeting and original message.
        """
        # Extract the message from args
        message = args.get("message", "World")
        
        # Log information about the execution
        self.logger.info(f"Processing message: {message}")
        
        # Return the result
        return {
            "greeting": f"Hello, {message}!",
            "original_message": message,
            "status": "success"
        }

# Initialize a singleton instance
example_tool = ExampleTool()

# Function to be registered in the tools/__init__.py
def example_tool_class(args: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper function for the ExampleTool execute method."""
    return example_tool.execute(args) 