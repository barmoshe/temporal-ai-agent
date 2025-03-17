#!/usr/bin/env python3
"""
Test script for the simplified tools - MIDI Creation Tool and Vanilla Tool
"""

import json
from tools import get_handler

def test_midi_tool():
    """Test the MIDI creation tool"""
    print("\nTesting MIDI Creation Tool...")
    
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
    
    # Get the tool handler
    midi_tool = get_handler("MidiCreationTool")
    
    # Call the tool
    result = midi_tool({
        "notes": json.dumps(test_notes),
        "tempo": 120,
        "title": "C Major Scale Test"
    })
    
    # Print results (excluding the base64 encoded data for clarity)
    if "error" in result:
        print(f"Error: {result['error']}")
        return False
    
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
    return True

def test_vanilla_tool():
    """Test the vanilla/fallback tool"""
    print("\nTesting Vanilla Tool...")
    
    # Get the tool handler
    vanilla_tool = get_handler("VanillaTool")
    
    # Call the tool
    result = vanilla_tool({
        "query": "Tell me about music composition",
        "context": "I'm interested in learning music theory"
    })
    
    # Print results
    if "error" in result:
        print(f"Error: {result['error']}")
        return False
    
    # Print the response
    print(f"Response ID: {result['response_id']}")
    print(f"Query: {result['query']}")
    print(f"Context: {result.get('context_provided', 'None')}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Response: {result['response']}")
    return True

def test_fallback():
    """Test the fallback mechanism for unknown tools"""
    print("\nTesting fallback mechanism...")
    
    # Try to get a non-existent tool (should fall back to VanillaTool)
    try:
        nonexistent_tool = get_handler("NonExistentTool")
        print("Successfully got fallback handler")
        
        # Call the tool
        result = nonexistent_tool({
            "query": "This is a test of the fallback mechanism",
        })
        
        # Print the response
        print(f"Response ID: {result['response_id']}")
        print(f"Response: {result['response']}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("===== Testing Simplified Tools =====")
    
    midi_success = test_midi_tool()
    vanilla_success = test_vanilla_tool()
    fallback_success = test_fallback()
    
    print("\n===== Test Results =====")
    print(f"MIDI Tool: {'PASS' if midi_success else 'FAIL'}")
    print(f"Vanilla Tool: {'PASS' if vanilla_success else 'FAIL'}")
    print(f"Fallback Mechanism: {'PASS' if fallback_success else 'FAIL'}")
    
    if midi_success and vanilla_success and fallback_success:
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed. Please check the output above for details.") 