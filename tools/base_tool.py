"""
Base Tool Class

This module provides a base class for tools to standardize error handling, logging, and other common functionality.
"""
import os
import json
import logging
import traceback
from typing import Dict, Any, Callable, TypeVar, cast
from functools import wraps
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Type variable for the tool function return type
T = TypeVar('T', bound=Dict[str, Any])

class BaseTool:
    """Base class for tools with standardized error handling and logging."""
    
    def __init__(self, name: str = None):
        """
        Initialize the tool with optional name.
        
        Args:
            name: Optional name for the tool (defaults to class name)
        """
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(f"tool.{self.name}")
        load_dotenv(override=True)
    
    def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool with error handling.
        
        Args:
            args: Dictionary of arguments for the tool.
            
        Returns:
            Dictionary containing the tool's response or error information.
        """
        try:
            self.logger.info(f"Executing tool {self.name} with args: {args}")
            result = self._execute(args)
            self.logger.info(f"Tool {self.name} execution completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error executing tool {self.name}: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {
                "error": str(e),
                "tool": self.name,
                "status": "error"
            }
    
    def _execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement this method in subclasses to provide tool-specific functionality.
        
        Args:
            args: Dictionary of arguments for the tool.
            
        Returns:
            Dictionary containing the tool's response.
        """
        raise NotImplementedError("Subclasses must implement _execute method")


def tool_function(f: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator for tool functions to add standardized error handling and logging.
    
    Example:
        @tool_function
        def my_tool(args: Dict[str, Any]) -> Dict[str, Any]:
            # Tool implementation
            return {"result": "success"}
    """
    @wraps(f)
    def wrapper(args: Dict[str, Any], *wargs, **kwargs) -> T:
        logger = logging.getLogger(f"tool.{f.__name__}")
        try:
            logger.info(f"Executing tool {f.__name__} with args: {args}")
            result = f(args, *wargs, **kwargs)
            logger.info(f"Tool {f.__name__} execution completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error executing tool {f.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            return cast(T, {
                "error": str(e),
                "tool": f.__name__,
                "status": "error"
            })
    return wrapper 