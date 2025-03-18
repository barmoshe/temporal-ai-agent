from .search_fixtures import search_fixtures
from .midi_creation_tool import midi_creation_tool
from .search_flights import search_flights
from .search_trains import search_trains
from .search_trains import book_trains
from .create_invoice import create_invoice
from .find_events import find_events
from .example_tool_class import example_tool_class
from .example_tool_function import example_tool_function
from .json_array_tool import create_json_array
from .default_chat_tool import default_chat
from .help_tool import help


def get_handler(tool_name: str):
    """
    Get the handler function for a tool by name.
    
    Args:
        tool_name: Name of the tool to get the handler for
        
    Returns:
        The handler function for the tool
        
    Raises:
        ValueError: If the tool name is not recognized
    """
    # Tool name to function mapping
    tool_handlers = {
        "DefaultChatTool": default_chat,
        "HelpTool": help,
        "SearchFixtures": search_fixtures,
        "SearchFlights": search_flights,
        "SearchTrains": search_trains,
        "BookTrains": book_trains,
        "CreateInvoice": create_invoice,
        "FindEvents": find_events,
        "ExampleToolClass": example_tool_class,
        "ExampleToolFunction": example_tool_function,
        "CreateJsonArray": create_json_array,
        "MidiCreationTool": midi_creation_tool,
    }
    
    # Get the handler function
    handler = tool_handlers.get(tool_name)
    
    # Raise an error if the tool name is not recognized
    if handler is None:
        available_tools = ", ".join(sorted(tool_handlers.keys()))
        raise ValueError(f"Unknown tool: {tool_name}. Available tools: {available_tools}")
    
    return handler
