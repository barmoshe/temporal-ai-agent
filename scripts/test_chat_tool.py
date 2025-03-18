"""
Test Chat Tool Script

This script demonstrates the usage of the DefaultChatTool.
It allows manual testing of the chat interface with and without triggering specialized tools.
"""
import sys
import os
import json
import logging
import uuid
from typing import Dict, Any

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import get_handler
from tools.chat_utils import format_help_response

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

def test_chat_tool() -> None:
    """Test the DefaultChatTool with various messages."""
    
    # Get the chat tool handler
    chat_handler = get_handler("DefaultChatTool")
    
    # Test message that should trigger flight search
    flight_message = "I want to book a flight from New York to London next week"
    print(f"\nTesting with message: '{flight_message}'")
    flight_result = chat_handler({"message": flight_message})
    print_json(flight_result)
    
    # Test message that should trigger event search
    event_message = "Are there any concerts in Melbourne in December?"
    print(f"\nTesting with message: '{event_message}'")
    event_result = chat_handler({"message": event_message})
    print_json(event_result)
    
    # Test message that should trigger MIDI creation
    midi_message = "Can you create a simple melody for me?"
    print(f"\nTesting with message: '{midi_message}'")
    midi_result = chat_handler({"message": midi_message})
    print_json(midi_result)
    
    # Test message that should trigger JSON array creation
    json_message = "Create a list of 5 tasks with schema of title, priority, and due date"
    print(f"\nTesting with message: '{json_message}'")
    json_result = chat_handler({"message": json_message})
    print_json(json_result)
    
    # Test help message
    help_message = "What can you help me with?"
    print(f"\nTesting with message: '{help_message}'")
    help_result = chat_handler({"message": help_message})
    print_json(help_result)
    
    # Test message that should not trigger any tool
    general_message = "Tell me about the weather today"
    print(f"\nTesting with message: '{general_message}'")
    general_result = chat_handler({"message": general_message})
    print_json(general_result)

def interactive_chat() -> None:
    """
    Start an interactive chat session with the DefaultChatTool.
    This allows for manual testing of the tool.
    """
    session_id = str(uuid.uuid4())
    conversation_history = []
    
    print("\n===== Interactive Chat Session =====")
    print("Type 'exit' to quit\n")
    
    # Get the chat tool handler
    chat_handler = get_handler("DefaultChatTool")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("\nEnding chat session")
            break
        
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        # Process message with the DefaultChatTool
        result = chat_handler({
            "message": user_input,
            "conversation_history": conversation_history
        })
        
        # Handle the response
        response = result.get("response", "")
        
        # Check if a tool was triggered
        if result.get("should_trigger_tool", False):
            tool_name = result.get("suggested_tool")
            tool_args = result.get("suggested_tool_args", {})
            
            print(f"\n[System: Triggering tool '{tool_name}' with args: {json.dumps(tool_args, indent=2)}]")
            
            # In a real implementation, you would execute the tool here
            # For this demo, we'll execute the tool directly to see the result
            tool_handler = get_handler(tool_name)
            tool_result = tool_handler(tool_args)
            
            # Special handling for HelpTool to make responses more conversational
            if tool_name == "HelpTool":
                formatted_response = format_help_response(response, tool_result)
                print(f"Assistant: {formatted_response}")
            else:
                print(f"Assistant: {response}")
                print(f"\n[Tool Result: {json.dumps(tool_result, indent=2)}]\n")
            
            # Add assistant response to history
            conversation_history.append({
                "role": "assistant", 
                "content": response + " " + json.dumps(tool_result)
            })
        else:
            # Direct response
            print(f"Assistant: {response}")
            
            # Add assistant response to history
            conversation_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_chat()
    else:
        test_chat_tool() 