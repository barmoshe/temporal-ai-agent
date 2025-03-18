"""
Test Help Tool Script

This script demonstrates the usage of the HelpTool both directly and through the DefaultChatTool.
It allows testing of various help queries to show the tool's capabilities.
"""
import sys
import os
import json
import logging
from typing import Dict, Any

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import get_handler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_json(data: Dict[str, Any]) -> None:
    """
    Print a dictionary as formatted JSON.
    
    Args:
        data: Dictionary to print
    """
    print(json.dumps(data, indent=2))

def test_help_tool_direct() -> None:
    """Test the HelpTool directly with various queries."""
    
    print("\n===== Testing HelpTool Directly =====")
    
    # Get the help tool handler
    help_handler = get_handler("HelpTool")
    
    # Test general help
    print("\nGeneral help (empty query):")
    general_result = help_handler({"query": ""})
    print_json(general_result)
    
    # Test listing all tools
    print("\nListing all tools:")
    list_result = help_handler({"query": "What tools are available?"})
    print_json(list_result)
    
    # Test specific tool info
    print("\nInformation about SearchFlights tool:")
    tool_result = help_handler({"query": "Tell me about the SearchFlights tool"})
    print_json(tool_result)
    
    # Test system info
    print("\nSystem information:")
    system_result = help_handler({"query": "Tell me about the system"})
    print_json(system_result)

def test_help_through_chat() -> None:
    """Test help functionality through the DefaultChatTool."""
    
    print("\n===== Testing Help Through DefaultChatTool =====")
    
    # Get the chat tool handler
    chat_handler = get_handler("DefaultChatTool")
    
    # Test simple help request
    help_message = "Help me"
    print(f"\nTesting with message: '{help_message}'")
    help_result = chat_handler({"message": help_message})
    print_json(help_result)
    
    # Test specific tool help request
    tool_help_message = "How do I use the SearchFlights tool?"
    print(f"\nTesting with message: '{tool_help_message}'")
    tool_help_result = chat_handler({"message": tool_help_message})
    print_json(tool_help_result)
    
    # Test what tools are available
    tools_message = "What can you do?"
    print(f"\nTesting with message: '{tools_message}'")
    tools_result = chat_handler({"message": tools_message})
    print_json(tools_result)

def interactive_help() -> None:
    """
    Start an interactive help session where users can ask help questions.
    """
    print("\n===== Interactive Help Session =====")
    print("Type 'exit' to quit\n")
    
    # Get the chat tool handler
    chat_handler = get_handler("DefaultChatTool")
    
    while True:
        user_input = input("Help query: ")
        
        if user_input.lower() == "exit":
            print("\nEnding help session")
            break
        
        # Process message with the DefaultChatTool
        # This will trigger HelpTool if it's a help request
        result = chat_handler({"message": user_input})
        
        # Check if a tool was triggered
        if result.get("should_trigger_tool", False):
            tool_name = result.get("suggested_tool")
            tool_args = result.get("suggested_tool_args", {})
            
            if tool_name == "HelpTool":
                # Execute the HelpTool directly
                help_handler = get_handler("HelpTool")
                help_result = help_handler(tool_args)
                
                # Print help information
                print(f"\n{help_result.get('result', '')}")
                
                # Handle different types of help responses
                if "tools" in help_result:
                    print("\nAvailable tools:")
                    for tool in help_result["tools"]:
                        print(f"- {tool['name']}: {tool['description']}")
                
                if "tool_name" in help_result:
                    print(f"\nTool: {help_result['tool_name']}")
                    print(f"Description: {help_result['description']}")
                    print("\nArguments:")
                    for arg in help_result["arguments"]:
                        print(f"- {arg['name']} ({arg['type']}): {arg['description']}")
                    print(f"\nUsage example: {help_result['usage_example']}")
                
                if "system_info" in help_result:
                    system_info = help_result["system_info"]
                    for key, value in system_info.items():
                        print(f"\n{key.capitalize()}: {value}")
                
                if "options" in help_result:
                    print("\nHelp options:")
                    for option in help_result["options"]:
                        print(f"- {option}")
                
                if "note" in help_result:
                    print(f"\nNote: {help_result['note']}")
            else:
                # If another tool was triggered, just show the response
                print(f"Assistant: {result.get('response', '')}")
                print(f"\n[System: Triggering tool '{tool_name}']")
        else:
            # Direct response
            print(f"Assistant: {result.get('response', '')}")

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_help()
    else:
        test_help_tool_direct()
        test_help_through_chat() 