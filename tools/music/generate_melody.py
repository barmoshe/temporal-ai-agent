import random
from typing import Dict, Any, List


def generate_melody(args: dict) -> dict:
    """
    Generates a melody based on specified parameters like key, scale, tempo, and mood.
    
    Args:
        args: Dictionary containing the following keys:
            - key: Musical key (e.g., 'C', 'F#', 'Bb')
            - scale: Musical scale (e.g., 'major', 'minor', 'dorian')
            - tempo: Tempo in BPM
            - mood: Emotional quality (e.g., 'happy', 'melancholic', 'energetic')
            - length: Optional length in bars (default: 8)
            
    Returns:
        Dictionary containing the generated melody information
    """
    key = args.get("key", "C")
    scale = args.get("scale", "major")
    tempo = int(args.get("tempo", 120))
    mood = args.get("mood", "happy")
    length = int(args.get("length", 8))
    
    # Generate a melody based on the parameters
    melody_notes = generate_melody_notes(key, scale, mood, length)
    
    # Create a melody description
    melody_description = f"Generated a {length}-bar {mood} melody in {key} {scale} at {tempo} BPM"
    
    # Generate a mock MIDI file path
    midi_file = f"/compositions/melodies/{key.replace('#', 'sharp').replace('b', 'flat')}_{scale}_{mood}_{tempo}bpm.mid"
    
    # Generate a mock audio preview path
    audio_preview = f"/compositions/previews/{key.replace('#', 'sharp').replace('b', 'flat')}_{scale}_{mood}_{tempo}bpm.mp3"
    
    return {
        "success": True,
        "melody_description": melody_description,
        "notes": melody_notes,
        "key": key,
        "scale": scale,
        "tempo": tempo,
        "mood": mood,
        "length": length,
        "midi_file": midi_file,
        "audio_preview": audio_preview
    }


def generate_melody_notes(key: str, scale: str, mood: str, length: int) -> List[str]:
    """
    Generate a sequence of notes for a melody based on music theory.
    
    Args:
        key: The musical key
        scale: The musical scale
        mood: The emotional mood
        length: Length in bars
        
    Returns:
        List of note names (e.g., ["C4", "E4", "G4"])
    """
    # Define the notes for each key
    key_notes = {
        "C": ["C", "D", "E", "F", "G", "A", "B"],
        "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
        "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
        "D": ["D", "E", "F#", "G", "A", "B", "C#"],
        "D#": ["D#", "E#", "F##", "G#", "A#", "B#", "C##"],
        "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
        "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
        "F": ["F", "G", "A", "Bb", "C", "D", "E"],
        "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
        "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
        "G": ["G", "A", "B", "C", "D", "E", "F#"],
        "G#": ["G#", "A#", "B#", "C#", "D#", "E#", "F##"],
        "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
        "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
        "A#": ["A#", "B#", "C##", "D#", "E#", "F##", "G##"],
        "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
        "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
        "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
    }
    
    # Define scale patterns (intervals from the root)
    scale_patterns = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "lydian": [0, 2, 4, 6, 7, 9, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "locrian": [0, 1, 3, 5, 6, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
        "blues": [0, 3, 5, 6, 7, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }
    
    # Use a simplified scale if the requested one isn't available
    if scale.lower() not in scale_patterns:
        scale = "major" if "maj" in scale.lower() else "minor"
    
    # Get the notes for the key
    base_notes = key_notes.get(key, key_notes["C"])
    
    # Generate a sequence of notes based on the mood
    notes = []
    
    # Different patterns based on mood
    if mood.lower() in ["happy", "energetic", "upbeat"]:
        # Happy melodies tend to use more major intervals and upward motion
        pattern_options = [
            [0, 2, 4, 2, 0, 2, 4, 7],  # Major triad with passing tones
            [0, 4, 7, 4, 2, 4, 0],     # Arpeggiated major chord
            [0, 2, 4, 5, 7, 5, 4, 2],  # Scale run with turn
        ]
    elif mood.lower() in ["sad", "melancholic", "somber"]:
        # Sad melodies tend to use minor intervals and downward motion
        pattern_options = [
            [0, -1, -3, -1, 0, -1, -3, -5],  # Minor descent
            [0, 3, 0, -2, 0, 3, 7, 3],       # Minor arpeggiation
            [7, 5, 3, 0, 3, 0, -2, 0],       # Descending minor pattern
        ]
    elif mood.lower() in ["mysterious", "tense", "suspenseful"]:
        # Mysterious melodies often use augmented or diminished intervals
        pattern_options = [
            [0, 1, 4, 1, 0, 6, 0, -1],       # Unusual intervals
            [0, 3, 6, 9, 6, 3, 0, -3],       # Diminished arpeggiation
            [0, 5, 6, 11, 6, 5, 0, -1],      # Augmented pattern
        ]
    else:  # Default/neutral mood
        pattern_options = [
            [0, 2, 4, 7, 4, 2, 0, 2],        # Basic pattern
            [0, 4, 7, 12, 7, 4, 0, -3],      # Wide range pattern
            [0, 2, 3, 5, 7, 8, 7, 5],        # Scale-based pattern
        ]
    
    # Choose a pattern and generate the melody
    pattern = random.choice(pattern_options)
    
    # Repeat the pattern to fill the requested length
    full_pattern = []
    bars_filled = 0
    while bars_filled < length:
        # Add some variation every other repeat
        if bars_filled > 0 and bars_filled % 2 == 0:
            # Modify a few notes in the pattern for variation
            modified_pattern = pattern.copy()
            for i in range(min(3, len(pattern))):
                idx = random.randint(0, len(pattern) - 1)
                modified_pattern[idx] = modified_pattern[idx] + random.choice([-2, -1, 1, 2])
            full_pattern.extend(modified_pattern)
        else:
            full_pattern.extend(pattern)
        bars_filled += 1
    
    # Convert the pattern to actual notes
    octave = 4  # Default octave
    current_position = 0
    
    for interval in full_pattern:
        # Adjust octave if needed
        new_position = current_position + interval
        if new_position >= 12:
            octave_shift = new_position // 12
            new_position = new_position % 12
            octave += octave_shift
        elif new_position < 0:
            octave_shift = (abs(new_position) + 11) // 12
            new_position = 12 - (abs(new_position) % 12)
            octave -= octave_shift
        
        # Get the note at this scale position
        scale_pos = scale_patterns.get(scale.lower(), scale_patterns["major"])[new_position % len(scale_patterns.get(scale.lower(), scale_patterns["major"]))]
        note_idx = scale_pos % 7
        note = base_notes[note_idx]
        
        # Add the note with octave
        notes.append(f"{note}{octave}")
        
        current_position = new_position
    
    return notes 