"""
MIDI Creation Tool

This tool converts a text representation of music (a list of note-duration tuples) 
into MIDI messages using the mido library.
"""
import os
import json
from dotenv import load_dotenv
from typing import Dict, Any, List, Tuple, Union
import mido
from .base_tool import tool_function

@tool_function
def midi_creation_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts a text representation of music into a list of MIDI messages.
    
    Args:
        args: Dictionary containing 'music_text', which is a list of tuples (note, duration).
              - note: int (valid range 21-108 for a note, or 0 for silence)
              - duration: float (between 0 and 2)
              
    Returns:
        A dictionary containing the generated MIDI messages and a status.
    """
    # Load environment variables if needed
    load_dotenv(override=True)
    
    # Extract arguments
    music_text = args.get("music_text")
    if music_text is None:  # Only error if music_text is completely missing, not if it's an empty list
        return {"error": "Missing 'music_text' argument", "status": "error"}
    
    midi_messages = []
    try:
        # Create a new MIDI file with one track
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)
        
        # Set tempo (120 BPM by default)
        tempo = mido.bpm2tempo(120)
        track.append(mido.MetaMessage('set_tempo', tempo=tempo))
        
        # Process each note-duration tuple
        for item in music_text:
            # Validate that item is a tuple or list of exactly two elements
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                return {
                    "error": f"Invalid format for item {item}. Expected a tuple of (note, duration).",
                    "status": "error"
                }
            
            note, duration = item
            # Validate note range (0 for silence, 21-108 for notes from A0 to C8)
            if note != 0 and not (21 <= note <= 108):
                return {
                    "error": f"Invalid note {note}. Must be 0 or between 21 and 108.",
                    "status": "error"
                }
            
            # Validate duration range (0 to 2 seconds)
            if not (0 <= duration <= 2):
                return {
                    "error": f"Invalid duration {duration}. Must be between 0 and 2.",
                    "status": "error"
                }
            
            # Convert duration to ticks (480 ticks per quarter note by default)
            # 1.0 duration = quarter note
            ticks = int(duration * 480)
            
            if note == 0:
                # Represent silence by just adding a delay
                # Add this as a special message type for the JSON output
                midi_messages.append({
                    "type": "delay",
                    "time": ticks,
                    "duration": duration
                })
                
                # For the actual MIDI file, just advance time
                if len(track) > 1:  # Only if we've already added at least one note
                    track[-1].time += ticks
            else:
                # Add note_on and note_off messages
                velocity = 64  # medium velocity
                
                # Create MIDI messages
                note_on = mido.Message('note_on', note=note, velocity=velocity, time=0)
                note_off = mido.Message('note_off', note=note, velocity=0, time=ticks)
                
                # Add to track
                track.append(note_on)
                track.append(note_off)
                
                # Add to JSON response
                midi_messages.append({
                    "type": "note_on",
                    "note": note,
                    "velocity": velocity,
                    "time": 0
                })
                midi_messages.append({
                    "type": "note_off",
                    "note": note,
                    "velocity": 0,
                    "time": ticks
                })
        
        # Save MIDI to a temporary file if needed
        # mid.save('output.mid')
        
        return {
            "result": midi_messages,
            "status": "success",
            "midi_data": {
                "format": mid.type,
                "ticks_per_beat": mid.ticks_per_beat,
                "tracks": len(mid.tracks),
                "messages_count": len(midi_messages)
            }
        }
    except Exception as e:
        return {"error": str(e), "status": "error"} 