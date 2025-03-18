# Tools Directory

This directory contains all the tools that can be used by the AI agent to perform actions in the system.

## Overview

Tools are functions that the AI agent can call to interact with external systems or perform specific tasks. Each tool is defined in the `tool_registry.py` file and implemented in its own file. The `__init__.py` file provides a mapping from tool names to their handler functions.

## Tool Structure

There are two supported approaches for implementing tools:

1. **Function-based approach** (with decorator): Simple, stateless tools that use the `@tool_function` decorator.
2. **Class-based approach**: More complex tools that need to maintain state or have more advanced functionality.

### Function-based Example

```python
from typing import Dict, Any
from .base_tool import tool_function

@tool_function
def my_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """Tool implementation."""
    # Tool implementation here
    return {"result": "success"}
```

### Class-based Example

```python
from typing import Dict, Any
from .base_tool import BaseTool

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(name="MyTool")
    
    def _execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        # Tool implementation here
        return {"result": "success"}

# Initialize a singleton instance
my_tool_instance = MyTool()

# Function to be registered in the tools/__init__.py
def my_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    return my_tool_instance.execute(args)
```

## Creating a New Tool

### Manual Process

1. Create a new Python file for your tool in the `tools` directory.
2. Implement your tool using either the function-based or class-based approach.
3. Add a tool definition to `tool_registry.py`.
4. Add your tool to the `get_handler` function in `__init__.py`.

### Automated Process (Recommended)

Use the `create_tool.py` script in the `scripts` directory:

```bash
python scripts/create_tool.py ToolName [arg1:type:description] [arg2:type:description] ...
```

Example:

```bash
python scripts/create_tool.py SearchHotels location:string:"Hotel location" checkin:ISO8601:"Check-in date"
```

This will:
1. Create a new tool file `tools/search_hotels.py`
2. Add the tool definition to `tool_registry.py`
3. Update `tools/__init__.py` with the new tool

## Tool Response Format

All tools should return a dictionary with the following structure:

```python
{
    # Tool-specific response data
    "key1": value1,
    "key2": value2,
    
    # Optional status information
    "status": "success"  # or "error"
}
```

In case of an error, the tool should return:

```python
{
    "error": "Error message",
    "tool": "ToolName",
    "status": "error"
}
```

## Best Practices

1. **Use the base tools**: Either extend `BaseTool` or use the `@tool_function` decorator for consistent error handling and logging.
2. **Document arguments**: Clearly document the expected arguments and their types in both the tool implementation and the tool definition.
3. **Validate inputs**: Check that all required arguments are present and valid before processing.
4. **Handle errors gracefully**: Catch exceptions and return meaningful error messages.
5. **Use environment variables**: For sensitive information like API keys, use environment variables loaded via `load_dotenv()`.
6. **Log appropriately**: Use the logger provided by the base tool to log important information.
7. **Keep tools focused**: Each tool should perform a single, well-defined task.
8. **Test thoroughly**: Create unit tests for your tools to ensure they work as expected.

## Example Tools

- `example_tool_class.py`: Demonstrates the class-based approach
- `example_tool_function.py`: Demonstrates the function-based approach
- `search_flights.py`: A more complex tool for searching flights 
- `midi_creation_tool.py`: Converts a list of note-duration tuples into MIDI messages

## Specific Tools Documentation

### MidiCreationTool

The MidiCreationTool converts a text representation of music into MIDI messages. It takes a list of note-duration tuples and creates a sequence of MIDI events.

#### Input Format

```python
{
    "music_text": [
        [60, 0.25],  # Middle C with a duration of a sixteenth note
        [0, 0.25],   # Silence for a sixteenth note
        [62, 0.5]    # D with a duration of an eighth note
    ]
}
```

Each tuple contains:
- **note**: An integer representing a MIDI note number (21-108, where 60 is middle C) or 0 for silence
- **duration**: A float between 0 and 2, where 1.0 represents a quarter note

#### Output Format

```python
{
    "result": [
        {"type": "note_on", "note": 60, "velocity": 64, "time": 0},
        {"type": "note_off", "note": 60, "velocity": 0, "time": 120},
        {"type": "delay", "time": 120, "duration": 0.25},
        {"type": "note_on", "note": 62, "velocity": 64, "time": 0},
        {"type": "note_off", "note": 62, "velocity": 0, "time": 240}
    ],
    "status": "success",
    "midi_data": {
        "format": 0,
        "ticks_per_beat": 480,
        "tracks": 1,
        "messages_count": 5
    }
}
```

The `result` field contains a list of MIDI messages with the following types:
- **note_on**: Starts a note with the specified note number and velocity
- **note_off**: Ends a note with the specified note number
- **delay**: Represents a silence/rest for the specified duration

The `midi_data` field provides metadata about the generated MIDI file.

#### Example Usage

```python
from tools.midi_creation_tool import midi_creation_tool

# Create a simple C major scale
result = midi_creation_tool({
    "music_text": [
        [60, 0.25],  # C
        [62, 0.25],  # D
        [64, 0.25],  # E
        [65, 0.25],  # F
        [67, 0.25],  # G
        [69, 0.25],  # A
        [71, 0.25],  # B
        [72, 0.5]    # C (octave up, longer duration)
    ]
})

# The result contains MIDI messages that can be used for playback or saved to a file
# using the mido library
``` 