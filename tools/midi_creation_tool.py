import json
import base64
import io
import uuid
from datetime import datetime
import mido


def midi_creation_tool(args: dict) -> dict:
    """
    Converts a text representation of music into MIDI notes.
    
    The input format is a list of (note, duration) tuples where:
    - note: integer between 21 (A0) and 96 (C7), or 0 for silence
    - duration: float between 0 and 2, representing note duration (common values: 0.125 for eighth note, 
      0.25 for quarter note, 0.5 for half note, 1 for whole note, 2 for double whole note)
    
    Returns a base64-encoded MIDI file and metadata.
    """
    # Extract arguments
    notes_str = args.get("notes", "")
    tempo = args.get("tempo", 120.0)
    title = args.get("title", f"Melody-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    
    try:
        # Parse notes - input should be a string representation of a list of (note, duration) tuples
        notes_data = json.loads(notes_str)
        
        if not isinstance(notes_data, list):
            return {"error": "Notes must be a list of (note, duration) tuples"}
        
        # Validate notes
        for i, note_item in enumerate(notes_data):
            if not isinstance(note_item, list) or len(note_item) != 2:
                return {"error": f"Note at index {i} is not a valid (note, duration) tuple"}
            
            note, duration = note_item
            
            # Validate note (0 for silence or 21-96 for actual notes)
            if not isinstance(note, int) or (note != 0 and (note < 21 or note > 96)):
                return {"error": f"Note at index {i} has invalid pitch value. Must be 0 (silence) or between 21 and 96"}
            
            # Validate duration
            if not isinstance(duration, (int, float)) or duration <= 0 or duration > 2:
                return {"error": f"Note at index {i} has invalid duration. Must be between 0 and 2"}
        
        # Create a new MIDI file (format 0 - single track)
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)
        
        # Set tempo (convert BPM to microseconds per beat)
        tempo_us = mido.bpm2tempo(float(tempo))
        track.append(mido.MetaMessage('set_tempo', tempo=tempo_us))
        
        # Add notes to the track
        current_time = 0
        
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
        
        # Generate a unique file ID
        file_id = f"MIDI-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        # Return structured response
        return {
            "file_id": file_id,
            "title": title,
            "tempo": tempo,
            "midi_base64": midi_base64,
            "note_count": len(notes_data),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "format_details": "MIDI format 0, single track",
            "notes_summary": [{"note": note, "duration": duration} for note, duration in notes_data[:5]] + (
                [{"note": "...", "duration": "..."}] if len(notes_data) > 5 else []
            )
        }
    
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format for notes"}
    except Exception as e:
        return {"error": f"Error creating MIDI file: {str(e)}"} 