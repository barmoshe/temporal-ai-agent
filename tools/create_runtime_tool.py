"""
Create Runtime Tool

This tool dynamically creates and registers new tools that can be used immediately
in the same conversation session.
"""
import json
import logging
import inspect
import importlib
import sys
from typing import Dict, Any, List
import ast
from .base_tool import tool_function, BaseTool
from models.tool_definitions import ToolDefinition, ToolArgument

# Create a logger for this tool
logger = logging.getLogger("tool.create_runtime_tool")

# Registry for runtime-created tools
RUNTIME_TOOLS = {}

def validate_code(code_str: str) -> bool:
    """
    Validate that the provided code is safe to execute.
    
    This is a basic implementation - a real version would need much more thorough
    security validation.
    """
    # Basic safety check - reject code with certain dangerous patterns
    dangerous_patterns = [
        "import os", "import sys", "import subprocess", 
        "exec(", "eval(", "__import__", "open(", 
        "os.system", "subprocess.run"
    ]
    
    for pattern in dangerous_patterns:
        if pattern in code_str:
            return False
    
    # Try parsing the code to make sure it's valid Python
    try:
        ast.parse(code_str)
        return True
    except SyntaxError:
        return False

def register_runtime_tool(tool_name: str, tool_func, tool_def: ToolDefinition) -> bool:
    """
    Register a dynamically created tool in the runtime registry.
    """
    from tools import get_handler
    
    # Add to our runtime tools registry
    RUNTIME_TOOLS[tool_name] = {
        "function": tool_func,
        "definition": tool_def
    }
    
    # Monkey patch the get_handler function to include our runtime tools
    original_get_handler = get_handler
    
    def patched_get_handler(name: str):
        if name in RUNTIME_TOOLS:
            return RUNTIME_TOOLS[name]["function"]
        return original_get_handler(name)
    
    # Replace the get_handler function
    setattr(importlib.import_module("tools"), "get_handler", patched_get_handler)
    
    logger.info(f"Registered runtime tool: {tool_name}")
    return True

@tool_function
def create_runtime_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dynamically create and register a new tool that can be used immediately
    in the current conversation.
    
    Args:
        args: Dictionary containing:
            - tool_name: CamelCase name for the new tool
            - description: Description of what the tool does
            - arguments: List of arguments objects (name, type, description)
            - implementation: Python code as string for the tool implementation
    
    Returns:
        Dictionary with status of tool creation
    """
    # Extract arguments
    tool_name = args.get("tool_name")
    description = args.get("description", f"Dynamically created {tool_name} tool")
    arguments = args.get("arguments", [])
    implementation = args.get("implementation", "")
    
    # Validate inputs
    if not tool_name or not implementation:
        return {
            "error": "Missing required parameters: tool_name and implementation",
            "status": "error"
        }
    
    # Validate the implementation code
    if not validate_code(implementation):
        return {
            "error": "Implementation code failed security validation",
            "status": "error"
        }
    
    # Create a unique module name for this tool
    module_name = f"dynamic_tool_{tool_name.lower()}"
    
    # Prepare the full code with imports and wrapping
    full_code = f"""
from typing import Dict, Any
from tools.base_tool import tool_function

@tool_function
def {tool_name.lower()}_implementation(args: Dict[str, Any]) -> Dict[str, Any]:
    # Dynamically created tool implementation
{implementation}
    """
    
    # Indent the implementation code
    indented_implementation = "\n".join(f"    {line}" for line in implementation.split("\n"))
    full_code = full_code.replace(implementation, indented_implementation)
    
    try:
        # Create a new module
        new_module = type(sys)(module_name)
        sys.modules[module_name] = new_module
        
        # Execute the code in the module namespace
        exec(full_code, new_module.__dict__)
        
        # Get the implementation function
        tool_func = getattr(new_module, f"{tool_name.lower()}_implementation")
        
        # Create tool arguments
        tool_args = []
        for arg in arguments:
            tool_args.append(ToolArgument(
                name=arg.get("name", ""),
                type=arg.get("type", "string"),
                description=arg.get("description", "")
            ))
        
        # Create tool definition
        tool_def = ToolDefinition(
            name=tool_name,
            description=description,
            arguments=tool_args
        )
        
        # Register the tool
        success = register_runtime_tool(tool_name, tool_func, tool_def)
        
        if success:
            return {
                "message": f"Tool {tool_name} created and registered successfully",
                "tool_name": tool_name,
                "status": "success"
            }
        else:
            return {
                "error": f"Failed to register tool {tool_name}",
                "status": "error"
            }
            
    except Exception as e:
        logger.error(f"Error creating runtime tool: {str(e)}")
        return {
            "error": f"Error creating tool: {str(e)}",
            "status": "error"
        } 