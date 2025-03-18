"""
Default Chat Tool

This module provides a default chat interface for the agent. It allows the agent to respond
to user queries directly without triggering other tools, or to decide which specialized tool to invoke.
"""
import re
import json
import logging
from typing import Dict, Any, List, Tuple, Optional
from .base_tool import BaseTool

class DefaultChatTool(BaseTool):
    """
    Default chat tool that serves as the main interface for the agent.
    
    This tool allows the agent to:
    1. Respond to user queries directly with conversation
    2. Analyze user intent and decide whether to trigger specialized tools
    """
    
    def __init__(self):
        """Initialize the default chat tool."""
        super().__init__(name="DefaultChatTool")
        self.known_tools = self._get_available_tools()
        
    def _get_available_tools(self) -> List[str]:
        """Get a list of available tools that can be triggered."""
        # Define a list of known tools that can be triggered
        # This avoids circular imports
        return [
            "SearchFlights",
            "SearchTrains",
            "BookTrains",
            "CreateInvoice",
            "FindEvents",
            "SearchFixtures",
            "ExampleToolClass",
            "ExampleToolFunction",
            "CreateJsonArray",
            "MidiCreationTool",
            "HelpTool"
        ]
    
    def _analyze_intent(self, message: str, history: List[Dict[str, Any]]) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Analyze the user's message to determine intent and whether to trigger a specialized tool.
        
        Args:
            message: The user's message
            history: Conversation history
            
        Returns:
            Tuple containing:
            - Boolean indicating if a tool should be triggered
            - Name of the tool to trigger (or None)
            - Arguments for the tool (or None)
        """
        # This is a simple rule-based implementation
        # In a production environment, this would use an LLM to analyze the intent
        
        message_lower = message.lower()
        
        # Check for help intent first
        if any(keyword in message_lower for keyword in ["help", "how do i", "what can you do", "?", "explain", "instructions", "guide", "tutorial"]):
            # If the message contains specific tool names, pass the query directly
            query = message
            
            # Check if it's a general help request
            if message_lower.strip() in ["help", "help me", "i need help", "what can you do"]:
                query = "list all tools"
                
            return True, "HelpTool", {
                "query": query
            }
        
        # Check for MIDI creation intent
        elif any(keyword in message_lower for keyword in ["midi", "music", "song", "melody", "tune", "compose"]):
            # Very simple example - in a real implementation, you would parse more complex music text
            # For testing purposes, let's create a basic scale
            return True, "MidiCreationTool", {
                "music_text": [
                    (60, 0.5),  # C4 (middle C) for half note
                    (62, 0.5),  # D4 for half note
                    (64, 0.5),  # E4 for half note
                    (65, 0.5),  # F4 for half note
                    (67, 0.5),  # G4 for half note
                    (69, 0.5),  # A4 for half note
                    (71, 0.5),  # B4 for half note
                    (72, 1.0)   # C5 for whole note
                ]
            }
        
        # Check for flight search intent
        elif any(keyword in message_lower for keyword in ["flight", "fly", "plane", "airport", "travel"]):
            # Extract potential origin and destination using simple pattern matching
            # This is very simplistic - a real implementation would use NLP/LLM
            from_match = re.search(r"from\s+([a-zA-Z\s]+)", message_lower)
            to_match = re.search(r"to\s+([a-zA-Z\s]+)", message_lower)
            
            if from_match and to_match:
                origin = from_match.group(1).strip()
                destination = to_match.group(1).strip()
                
                return True, "SearchFlights", {
                    "origin": origin,
                    "destination": destination,
                    # Date parameters would need more sophisticated parsing
                    "dateDepart": "2023-11-01",  # Placeholder
                    "dateReturn": "2023-11-08"   # Placeholder
                }
        
        # Check for event search intent
        elif any(keyword in message_lower for keyword in ["event", "concert", "show", "performance"]):
            city_match = re.search(r"in\s+([a-zA-Z\s]+)", message_lower)
            month_match = re.search(r"(january|february|march|april|may|june|july|august|september|october|november|december)", message_lower)
            
            if city_match and month_match:
                city = city_match.group(1).strip()
                month = month_match.group(1).strip()
                
                return True, "FindEvents", {
                    "city": city,
                    "month": month
                }
        
        # Check for JSON array creation intent
        elif any(keyword in message_lower for keyword in ["json", "array", "list", "create list", "generate data"]):
            prompt = message
            schema = ""
            
            # Extract schema if specified
            schema_match = re.search(r"with\s+schema\s+(.*)", message_lower)
            if schema_match:
                schema = schema_match.group(1).strip()
                # Remove schema part from prompt
                prompt = re.sub(r"with\s+schema\s+.*", "", prompt).strip()
            
            return True, "CreateJsonArray", {
                "prompt": prompt,
                "schema": schema
            }
        
        # Add more intent detection rules for other tools
        
        # Default: No specialized tool needed
        return False, None, None
    
    def _execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the user's message and determine the appropriate response.
        
        Args:
            args: Dictionary containing:
                - 'message': The user's message
                - 'conversation_history': Optional conversation history for context
                
        Returns:
            Dictionary containing:
                - 'response': The agent's response
                - 'should_trigger_tool': Boolean indicating if a specialized tool should be triggered
                - 'suggested_tool': Name of the suggested tool (if any)
                - 'suggested_tool_args': Arguments for the suggested tool (if any)
                - 'status': Success or error status
        """
        # Extract the message from args
        message = args.get("message", "")
        conversation_history = args.get("conversation_history", [])
        
        if not message:
            return {
                "response": "I didn't receive a message to process.",
                "should_trigger_tool": False,
                "status": "error"
            }
        
        # Log information about the execution
        self.logger.info(f"Processing message: {message}")
        
        # Analyze intent to determine if a specialized tool should be triggered
        should_trigger, tool_name, tool_args = self._analyze_intent(message, conversation_history)
        
        if should_trigger and tool_name:
            self.logger.info(f"Determined intent: trigger {tool_name}")
            
            # Special handling for help tool to make it more conversational
            if tool_name == "HelpTool":
                response_prefix = "I'll help you with that. "
            else:
                response_prefix = f"I'll help you with that by using our {tool_name} capability."
                
            # Return with suggestion to trigger the specialized tool
            return {
                "response": response_prefix,
                "should_trigger_tool": True,
                "suggested_tool": tool_name,
                "suggested_tool_args": tool_args,
                "status": "success"
            }
        
        # No specialized tool needed, generate a direct response
        # In a real implementation, this would use an LLM to generate the response
        response = f"I received your message: '{message}'. How can I assist you further?"
        
        # Return with direct response
        return {
            "response": response,
            "should_trigger_tool": False,
            "suggested_tool": None,
            "suggested_tool_args": None,
            "status": "success"
        }

# Initialize a singleton instance
default_chat_tool = DefaultChatTool()

# Function to be registered in the tools/__init__.py
def default_chat(args: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper function for the DefaultChatTool execute method."""
    return default_chat_tool.execute(args) 