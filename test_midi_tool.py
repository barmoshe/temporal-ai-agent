#!/usr/bin/env python
"""
Test script for the MidiCreationTool

This script creates a simple C major scale as a test MIDI file
"""

import json
import sys
from tools.midi_creation_tool import midi_creation_tool

# Create a simple C major scale (C4 to C5)
# C D E F G A B C
# MIDI notes: 60, 62, 64, 65, 67, 69, 71, 72
# Each note will be a quarter note (0.25)
test_notes = [
    [60, 0.25],  # C4
    [62, 0.25],  # D4
    [64, 0.25],  # E4
    [65, 0.25],  # F4
    [67, 0.25],  # G4
    [69, 0.25],  # A4
    [71, 0.25],  # B4
    [72, 0.5],   # C5 (longer, half note)
]

# Convert to JSON string (how it would be passed in actual use)
notes_json = json.dumps(test_notes)

# Call the tool
result = midi_creation_tool({
    "notes": notes_json,
    "tempo": 120,
    "title": "C Major Scale Test"
})

# Print results (excluding the base64 encoded data for clarity)
if "error" in result:
    print(f"Error: {result['error']}")
    sys.exit(1)

# Print a success message with metadata
print(f"MIDI file created successfully!")
print(f"Title: {result['title']}")
print(f"File ID: {result['file_id']}")
print(f"Note count: {result['note_count']}")
print(f"Created at: {result['created_at']}")
print(f"Format: {result['format_details']}")
print("\nNotes summary:")
for note in result['notes_summary']:
    if isinstance(note['note'], int):
        print(f"  Note: {note['note']} (Duration: {note['duration']})")
    else:
        print(f"  {note['note']} {note['duration']}")

# Length of base64 data to verify it was generated
print(f"\nBase64 MIDI data length: {len(result['midi_base64'])} characters")

print("\nTest completed successfully!") 