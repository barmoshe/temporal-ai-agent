#!/usr/bin/env python3
"""
Direct test for MIDI creation functionality without importing the full tools module
"""

import json
import base64
import io
import uuid
from datetime import datetime
import mido


def test_midi_creation(notes_data, tempo=120.0, title="Test Melody"):
    """
    Test function to create a MIDI file from a list of (note, duration) tuples
    """
    try:
        # Create a new MIDI file (format 0 - single track)
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)
        
        # Set tempo (convert BPM to microseconds per beat)
        tempo_us = mido.bpm2tempo(float(tempo))
        track.append(mido.MetaMessage('set_tempo', tempo=tempo_us))
        
        # Add notes to the track
        for note_value, duration in notes_data:
            # Convert duration to ticks (assuming quarter note = 0.25)
            ticks_per_beat = mid.ticks_per_beat
            duration_ticks = int(duration * 4 * ticks_per_beat)  # 4 = beats per whole note
            
            if note_value > 0:  # Skip if it's a silence (note value 0)
                # Note on event
                track.append(mido.Message('note_on', note=note_value, velocity=64, time=0))
                # Note off event (after duration)
                track.append(mido.Message('note_off', note=note_value, velocity=64, time=duration_ticks))
            else:
                # For silence, add a dummy event with the duration
                track.append(mido.MetaMessage('text', text='silence', time=duration_ticks))
        
        # Save MIDI to in-memory buffer
        buffer = io.BytesIO()
        mid.save(file=buffer)
        buffer.seek(0)
        
        # Convert to base64
        midi_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        return {
            "title": title,
            "tempo": tempo,
            "midi_base64": midi_base64,
            "note_count": len(notes_data),
            "success": True
        }
    
    except Exception as e:
        return {"error": f"Error creating MIDI file: {str(e)}", "success": False}


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

if __name__ == "__main__":
    # Call the test function
    result = test_midi_creation(test_notes, 120, "C Major Scale Test")
    
    if not result.get("success", False):
        print(f"Error: {result.get('error', 'Unknown error')}")
        exit(1)
    
    # Save the MIDI file for verification
    midi_data = base64.b64decode(result["midi_base64"])
    with open("test_scale.mid", "wb") as f:
        f.write(midi_data)
    
    # Print success info
    print(f"MIDI file created successfully!")
    print(f"Title: {result['title']}")
    print(f"Note count: {result['note_count']}")
    print(f"Saved as: test_scale.mid")
    print(f"\nBase64 MIDI data length: {len(result['midi_base64'])} characters")
    
    print("\nTest completed successfully!") 