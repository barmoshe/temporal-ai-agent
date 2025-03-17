from .midi_creation_tool import midi_creation_tool
from .vanilla_tool import vanilla_tool


def get_handler(tool_name: str):
    if tool_name == "MidiCreationTool":
        return midi_creation_tool
    if tool_name == "VanillaTool":
        return vanilla_tool

    # If no matching tool, use the vanilla tool as a fallback
    # but first log the unknown tool for debugging
    print(f"WARNING: Unknown tool requested: {tool_name}. Using VanillaTool as fallback.")
    return vanilla_tool
