"""
Help Tool

This module provides a help tool that can explain available tools and answer system questions.
"""
import re
import json
import logging
from typing import Dict, Any, List, Optional
from .base_tool import BaseTool

class HelpTool(BaseTool):
    """
    Help tool that provides information about available tools and the system.
    
    This tool can:
    1. List all available tools
    2. Provide detailed information about specific tools
    3. Answer general questions about the system
    """
    
    def __init__(self):
        """Initialize the help tool."""
        super().__init__(name="HelpTool")
        self.tool_descriptions = self._get_tool_descriptions()
        
    def _get_tool_descriptions(self) -> Dict[str, Dict[str, Any]]:
        """Get descriptions of all available tools."""
        # Import here to avoid circular imports
        from models.tool_definitions import ToolDefinition, ToolArgument
        from tools.tool_registry import (
            default_chat_tool, midicreationtool_tool, json_array_tool,
            search_flights_tool, example_tool_class_tool, example_tool_function_tool,
            search_trains_tool, book_trains_tool, create_invoice_tool,
            search_fixtures_tool, find_events_tool
        )
        
        # Collect all tool definitions
        tools = {
            "DefaultChatTool": default_chat_tool,
            "MidiCreationTool": midicreationtool_tool,
            "CreateJsonArray": json_array_tool,
            "SearchFlights": search_flights_tool,
            "ExampleToolClass": example_tool_class_tool,
            "ExampleToolFunction": example_tool_function_tool,
            "SearchTrains": search_trains_tool,
            "BookTrains": book_trains_tool,
            "CreateInvoice": create_invoice_tool,
            "SearchFixtures": search_fixtures_tool,
            "FindEvents": find_events_tool,
            "HelpTool": {
                "name": "HelpTool",
                "description": "Provides information about available tools and answers questions about the system.",
                "arguments": [
                    {
                        "name": "query",
                        "type": "string",
                        "description": "The help query (e.g., 'list all tools', 'how to use SearchFlights', etc.)"
                    }
                ]
            }
        }
        
        return tools
    
    def _get_system_info(self) -> Dict[str, str]:
        """Get general information about the system."""
        return {
            "name": "Temporal AI Agent",
            "description": "An AI agent system that uses Temporal workflows to orchestrate tool execution.",
            "capabilities": "The system can handle various tasks through specialized tools, including searching for flights and events, creating MIDI music, generating JSON data, and more.",
            "interaction": "You can interact with the system through natural language. The DefaultChatTool will analyze your request and either respond directly or trigger the appropriate specialized tool."
        }
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse the help query to determine what information is being requested.
        
        Args:
            query: The help query
            
        Returns:
            Dictionary containing the parsed query information
        """
        query_lower = query.lower()
        
        # Check if the query is asking for a list of all tools
        if any(pattern in query_lower for pattern in [
            "list all tools", "show tools", "available tools", "what tools", 
            "what can you do", "capabilities", "what are the tools"
        ]):
            return {
                "type": "list_tools",
                "filter": None
            }
        
        # Check if the query is asking about a specific tool
        for tool_name in self.tool_descriptions.keys():
            tool_name_lower = tool_name.lower()
            if tool_name_lower in query_lower or f"how to use {tool_name_lower}" in query_lower:
                return {
                    "type": "tool_info",
                    "tool_name": tool_name
                }
        
        # Check if the query is about the system
        if any(pattern in query_lower for pattern in [
            "about the system", "system info", "how does it work", 
            "what is this", "tell me about", "the agent"
        ]):
            return {
                "type": "system_info",
                "aspect": None  # Could be more specific in a more advanced implementation
            }
        
        # Default to general help
        return {
            "type": "general_help",
            "query": query
        }
    
    def _execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the help query and provide the appropriate information.
        
        Args:
            args: Dictionary containing the 'query' parameter
                
        Returns:
            Dictionary containing the help information
        """
        # Extract the query from args
        query = args.get("query", "")
        
        if not query:
            # Default help if no query is provided
            return self._provide_general_help()
        
        # Log information about the execution
        self.logger.info(f"Processing help query: {query}")
        
        # Parse the query to determine what information is being requested
        parsed_query = self._parse_query(query)
        
        # Provide the appropriate information based on the parsed query
        if parsed_query["type"] == "list_tools":
            return self._list_all_tools()
        elif parsed_query["type"] == "tool_info":
            return self._provide_tool_info(parsed_query["tool_name"])
        elif parsed_query["type"] == "system_info":
            return self._provide_system_info()
        else:
            return self._provide_general_help()
    
    def _list_all_tools(self) -> Dict[str, Any]:
        """
        List all available tools with brief descriptions.
        
        Returns:
            Dictionary containing the list of tools
        """
        tools_list = []
        
        for tool_name, tool_def in self.tool_descriptions.items():
            # Skip the DefaultChatTool in the list as it's the main interface
            if tool_name != "DefaultChatTool":
                tools_list.append({
                    "name": tool_name,
                    "description": tool_def.get("description", "") if isinstance(tool_def, dict) else tool_def.description
                })
        
        # Sort tools by name
        tools_list = sorted(tools_list, key=lambda x: x["name"])
        
        return {
            "result": "Here are the available tools:",
            "tools": tools_list,
            "info": "You can ask for more details about a specific tool by saying 'help with [tool name]'.",
            "status": "success"
        }
    
    def _provide_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """
        Provide detailed information about a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dictionary containing the tool information
        """
        tool_def = self.tool_descriptions.get(tool_name)
        
        if not tool_def:
            return {
                "error": f"Tool '{tool_name}' not found.",
                "status": "error"
            }
        
        # Extract tool details
        description = tool_def.get("description", "") if isinstance(tool_def, dict) else tool_def.description
        
        # Extract arguments
        if isinstance(tool_def, dict):
            arguments = tool_def.get("arguments", [])
            args_info = []
            for arg in arguments:
                args_info.append({
                    "name": arg.get("name", ""),
                    "type": arg.get("type", ""),
                    "description": arg.get("description", "")
                })
        else:
            args_info = [{
                "name": arg.name,
                "type": arg.type,
                "description": arg.description
            } for arg in tool_def.arguments]
        
        return {
            "result": f"Information about the {tool_name} tool:",
            "tool_name": tool_name,
            "description": description,
            "arguments": args_info,
            "usage_example": self._get_usage_example(tool_name),
            "status": "success"
        }
    
    def _provide_system_info(self) -> Dict[str, Any]:
        """
        Provide general information about the system.
        
        Returns:
            Dictionary containing the system information
        """
        system_info = self._get_system_info()
        
        return {
            "result": "About the Temporal AI Agent system:",
            "system_info": system_info,
            "status": "success"
        }
    
    def _provide_general_help(self) -> Dict[str, Any]:
        """
        Provide general help information.
        
        Returns:
            Dictionary containing general help information
        """
        return {
            "result": "How to get help with the Temporal AI Agent:",
            "options": [
                "List all tools: 'What tools are available?'",
                "Tool information: 'Help with SearchFlights'",
                "System information: 'Tell me about the system'",
                "Specific questions: 'How do I book a flight?'"
            ],
            "note": "You can also interact directly with the system by stating your request, and the DefaultChatTool will determine whether to respond directly or use a specialized tool.",
            "status": "success"
        }
    
    def _get_usage_example(self, tool_name: str) -> str:
        """
        Get a usage example for a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            String containing a usage example
        """
        examples = {
            "SearchFlights": "I want to book a flight from New York to London next week",
            "FindEvents": "Are there any concerts in Melbourne in December?",
            "MidiCreationTool": "Create a simple melody for me",
            "CreateJsonArray": "Generate a list of 5 tasks with schema of title, priority, and due date",
            "SearchTrains": "I need to find a train from London to Manchester tomorrow morning",
            "BookTrains": "Book the 9:30 train from London to Manchester",
            "CreateInvoice": "Create an invoice for my flight booking for $500",
            "SearchFixtures": "What are the upcoming fixtures for Manchester United?",
            "HelpTool": "What tools are available?"
        }
        
        return examples.get(tool_name, f"Ask the system to use the {tool_name} tool")

# Initialize a singleton instance
help_tool = HelpTool()

# Function to be registered in the tools/__init__.py
def help(args: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper function for the HelpTool execute method."""
    return help_tool.execute(args) 