from models.tool_definitions import ToolDefinition, ToolArgument

# MIDI Creation Tool
midi_creation_tool = ToolDefinition(
    name="MidiCreationTool",
    description="Converts a text representation of music into MIDI notes. Used for creating simple musical sequences that can be played by the frontend.",
    arguments=[
        ToolArgument(
            name="notes",
            type="string",
            description="A text representation of music notes in JSON format. Each note is a tuple of (note, duration) where note is an integer between 21 and 96 (or 0 for silence) and duration is a float between 0 and 2.",
        ),
        ToolArgument(
            name="tempo",
            type="float",
            description="Optional: The tempo in BPM for the MIDI file. Defaults to 120 BPM.",
        ),
        ToolArgument(
            name="title",
            type="string",
            description="Optional: A title for the MIDI sequence.",
        ),
    ],
)

# Vanilla Tool (Fallback)
vanilla_tool = ToolDefinition(
    name="VanillaTool",
    description="A general-purpose fallback tool for when no specific tool fits the requirements. Use this tool for any request that doesn't match other specialized tools.",
    arguments=[
        ToolArgument(
            name="query",
            type="string",
            description="The user's query or request that needs to be processed",
        ),
        ToolArgument(
            name="context",
            type="string",
            description="Optional: Additional context or background information related to the query",
        ),
    ],
) 