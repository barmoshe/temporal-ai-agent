from models.tool_definitions import AgentGoal
from tools.tool_registry import (
    midi_creation_tool,
    vanilla_tool,
)

# Define a single simple goal with our two tools
goal_simple_music = AgentGoal(
    tools=[
        midi_creation_tool,
        vanilla_tool,
    ],
    description="Help the user create simple musical sequences using MIDI or handle general-purpose requests. "
    "Available tools: "
    "1. MidiCreationTool: Convert a text representation of music into MIDI notes that can be played by the frontend. "
    "2. VanillaTool: A fallback for general-purpose requests that don't fit other tools.",
    starter_prompt="Welcome! I can help you create simple musical sequences using MIDI, or assist with general questions. What would you like to do today?",
    example_conversation_history="\n ".join(
        [
            "user: I want to create a simple melody",
            "agent: I'd be happy to help you create a simple melody! I can convert a sequence of notes to MIDI format that the frontend can play. Would you like to specify the notes and durations yourself, or would you like me to suggest a simple pattern?",
            "user: Can you suggest a pattern for a happy tune?",
            "agent: Of course! For a happy tune, let's create a simple C major melody. Here's what I suggest: I'll create a sequence with these notes: C4 (60), E4 (64), G4 (67), C5 (72), G4 (67), E4 (64), C4 (60), with quarter and eighth note durations to give it a cheerful bounce. Would you like me to generate this MIDI sequence for you?",
            "user: Yes, please!",
            "user_confirmed_tool_run: <user clicks confirm on MidiCreationTool>",
            'tool_result: {"file_id": "MIDI-20250704-a1b2c3d4", "title": "Happy C Major Melody", "tempo": 120, "midi_base64": "TVRoZAAAAAYAAQAEA8BNVHJrAAAATwD/UQMHoSAA/1gEBAIYCACBAIEAnEAgAJxALAA8QCCcQCwAP0AgnEAsAENAIJxALABIQCCcQCwAQ0AgnEAsAD9AIJxALAA8QCCQAFgA/y8A", "note_count": 7, "created_at": "2025-07-04 10:15:30", "format_details": "MIDI format 0, single track", "notes_summary": [{"note": 60, "duration": 0.25}, {"note": 64, "duration": 0.25}, {"note": 67, "duration": 0.25}, {"note": 72, "duration": 0.5}, {"note": 67, "duration": 0.25}, {"note": 64, "duration": 0.25}, {"note": 60, "duration": 0.25}]}',
            "agent: I've created a happy C major melody for you! You can see and play the melody as colorful bubbles in the player above. Each bubble represents a note, with larger bubbles indicating longer durations. The sequence has 7 notes at a tempo of 120 BPM. Click the play button to hear the melody! Would you like to create another melody or make adjustments to this one?",
            "user: Can you create a simple scale that goes up and down?",
            "agent: I'd be happy to create a simple scale that goes up and down for you! I'll create a C major scale (C4 to C5) that ascends and then descends. Each note will be a quarter note (0.25 duration). Would you like me to generate this MIDI sequence for you?",
            "user: Yes, please generate it",
            "user_confirmed_tool_run: <user clicks confirm on MidiCreationTool>",
            'tool_result: {"file_id": "MIDI-20250704-b5f7e9d1", "title": "C Major Scale Up and Down", "tempo": 120, "midi_base64": "TVRoZAAAAAYAAQAEA8BNVHJrAAAAdQD/UQMHoSAA/1gEBAIYCACSAIEAnEAgAJxALAA8QCCcQCwAPkAgnEAsAEBAIJxALABCQCCcQCwAREAgnEAsAEVAIJxALABHQCCcQCwAQ0AgnEAsAENAIJxALABCQCCcQCwAQEAgnEAsAD5AIJxALAA8QCCQAFgA/y8A", "note_count": 15, "created_at": "2025-07-04 10:18:45", "format_details": "MIDI format 0, single track", "notes_summary": [{"note": 60, "duration": 0.25}, {"note": 62, "duration": 0.25}, {"note": 64, "duration": 0.25}, {"note": 65, "duration": 0.25}, {"note": 67, "duration": 0.25}, {"note": "...", "duration": "..."}]}',
            "agent: I've created a C major scale that goes up and down! The bubble player shows the sequence where each bubble represents a note - you can see how they increase in pitch (going up the scale) and then decrease (coming down). The melody contains 15 notes, including all the notes of the C major scale ascending (C4, D4, E4, F4, G4, A4, B4, C5) and then descending (C5, B4, A4, G4, F4, E4, D4, C4). Click the play button to hear it! Would you like to try creating something else?",
            "user: Can you tell me about music theory?",
            "user_confirmed_tool_run: <user clicks confirm on VanillaTool>",
            'tool_result: {"response_id": "VANILLA-20250704101822", "query": "Can you tell me about music theory?", "response": "I received your request: \'Can you tell me about music theory?\'. However, I don\'t have a specialized tool for this specific task. I\'ll do my best to help using my general knowledge.", "timestamp": "2025-07-04 10:18:22"}',
            "agent: Music theory is the study of the practices and possibilities of music. It encompasses the elements of music - rhythm, harmony, melody, structure, and expression. The basic components include: 1) Notes and scales: The fundamental pitches and their organization into sequences, 2) Intervals: The relationships between pitches, 3) Chords: Multiple notes played simultaneously, 4) Key signatures and tonality: The organization of music around central pitches, and 5) Rhythm and meter: The organization of music in time. Would you like me to explain any specific aspect of music theory in more detail?",
        ]
    ),
) 