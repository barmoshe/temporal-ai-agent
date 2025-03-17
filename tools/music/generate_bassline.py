import random
from typing import Dict, Any, List


def generate_bassline(args: dict) -> dict:
    """
    Generates a bassline that complements a given chord progression.
    
    Args:
        args: Dictionary containing the following keys:
            - chords: Comma-separated list of chord symbols (e.g., 'Cmaj7,Am7,Fmaj7,G7')
            - style: Bass style (e.g., 'walking', 'funk', 'rock')
            - tempo: Tempo in BPM
            
    Returns:
        Dictionary containing the generated bassline information
    """
    chords_str = args.get("chords", "C,F,G,C")
    style = args.get("style", "rock")
    tempo = int(args.get("tempo", 120))
    
    # Parse the chord list
    chords = [c.strip() for c in chords_str.split(",") if c.strip()]
    
    # Generate a bassline based on the parameters
    notes, pattern = generate_bassline_notes(chords, style)
    
    # Create a bassline description
    bassline_description = f"Generated a {style} bassline for the chord progression {', '.join(chords)} at {tempo} BPM"
    
    # Generate a mock MIDI file path
    midi_file = f"/compositions/basslines/{style}_{tempo}bpm.mid"
    
    # Generate a mock audio preview path
    audio_preview = f"/compositions/previews/bass_{style}_{tempo}bpm.mp3"
    
    return {
        "success": True,
        "bassline_description": bassline_description,
        "notes": notes,
        "pattern": pattern,
        "chords": chords,
        "style": style,
        "tempo": tempo,
        "midi_file": midi_file,
        "audio_preview": audio_preview
    }


def generate_bassline_notes(chords: List[str], style: str) -> tuple:
    """
    Generate a sequence of bass notes based on the chord progression and style.
    
    Args:
        chords: List of chord symbols
        style: Bass playing style
        
    Returns:
        Tuple of (notes_list, pattern_description)
    """
    # Define the notes for each chord
    chord_notes = {
        # Major chords
        "C": ["C2", "E2", "G2"],
        "C#": ["C#2", "E#2", "G#2"],
        "Db": ["Db2", "F2", "Ab2"],
        "D": ["D2", "F#2", "A2"],
        "D#": ["D#2", "F##2", "A#2"],
        "Eb": ["Eb2", "G2", "Bb2"],
        "E": ["E2", "G#2", "B2"],
        "F": ["F2", "A2", "C3"],
        "F#": ["F#2", "A#2", "C#3"],
        "Gb": ["Gb2", "Bb2", "Db3"],
        "G": ["G2", "B2", "D3"],
        "G#": ["G#2", "B#2", "D#3"],
        "Ab": ["Ab2", "C3", "Eb3"],
        "A": ["A2", "C#3", "E3"],
        "A#": ["A#2", "C##3", "E#3"],
        "Bb": ["Bb2", "D3", "F3"],
        "B": ["B2", "D#3", "F#3"],
        
        # Minor chords
        "Cm": ["C2", "Eb2", "G2"],
        "C#m": ["C#2", "E2", "G#2"],
        "Dbm": ["Db2", "Fb2", "Ab2"],
        "Dm": ["D2", "F2", "A2"],
        "D#m": ["D#2", "F#2", "A#2"],
        "Ebm": ["Eb2", "Gb2", "Bb2"],
        "Em": ["E2", "G2", "B2"],
        "Fm": ["F2", "Ab2", "C3"],
        "F#m": ["F#2", "A2", "C#3"],
        "Gbm": ["Gb2", "Bbb2", "Db3"],
        "Gm": ["G2", "Bb2", "D3"],
        "G#m": ["G#2", "B2", "D#3"],
        "Abm": ["Ab2", "Cb3", "Eb3"],
        "Am": ["A2", "C3", "E3"],
        "A#m": ["A#2", "C#3", "E#3"],
        "Bbm": ["Bb2", "Db3", "F3"],
        "Bm": ["B2", "D3", "F#3"],
        
        # Dominant 7th chords
        "C7": ["C2", "E2", "G2", "Bb2"],
        "C#7": ["C#2", "E#2", "G#2", "B2"],
        "D7": ["D2", "F#2", "A2", "C3"],
        "D#7": ["D#2", "F##2", "A#2", "C#3"],
        "Eb7": ["Eb2", "G2", "Bb2", "Db3"],
        "E7": ["E2", "G#2", "B2", "D3"],
        "F7": ["F2", "A2", "C3", "Eb3"],
        "F#7": ["F#2", "A#2", "C#3", "E3"],
        "G7": ["G2", "B2", "D3", "F3"],
        "G#7": ["G#2", "B#2", "D#3", "F#3"],
        "Ab7": ["Ab2", "C3", "Eb3", "Gb3"],
        "A7": ["A2", "C#3", "E3", "G3"],
        "Bb7": ["Bb2", "D3", "F3", "Ab3"],
        "B7": ["B2", "D#3", "F#3", "A3"],
        
        # Major 7th chords
        "Cmaj7": ["C2", "E2", "G2", "B2"],
        "C#maj7": ["C#2", "E#2", "G#2", "B#2"],
        "Dmaj7": ["D2", "F#2", "A2", "C#3"],
        "Ebmaj7": ["Eb2", "G2", "Bb2", "D3"],
        "Emaj7": ["E2", "G#2", "B2", "D#3"],
        "Fmaj7": ["F2", "A2", "C3", "E3"],
        "F#maj7": ["F#2", "A#2", "C#3", "E#3"],
        "Gmaj7": ["G2", "B2", "D3", "F#3"],
        "Abmaj7": ["Ab2", "C3", "Eb3", "G3"],
        "Amaj7": ["A2", "C#3", "E3", "G#3"],
        "Bbmaj7": ["Bb2", "D3", "F3", "A3"],
        "Bmaj7": ["B2", "D#3", "F#3", "A#3"],
        
        # Minor 7th chords
        "Cm7": ["C2", "Eb2", "G2", "Bb2"],
        "C#m7": ["C#2", "E2", "G#2", "B2"],
        "Dm7": ["D2", "F2", "A2", "C3"],
        "D#m7": ["D#2", "F#2", "A#2", "C#3"],
        "Ebm7": ["Eb2", "Gb2", "Bb2", "Db3"],
        "Em7": ["E2", "G2", "B2", "D3"],
        "Fm7": ["F2", "Ab2", "C3", "Eb3"],
        "F#m7": ["F#2", "A2", "C#3", "E3"],
        "Gm7": ["G2", "Bb2", "D3", "F3"],
        "G#m7": ["G#2", "B2", "D#3", "F#3"],
        "Abm7": ["Ab2", "Cb3", "Eb3", "Gb3"],
        "Am7": ["A2", "C3", "E3", "G3"],
        "Bbm7": ["Bb2", "Db3", "F3", "Ab3"],
        "Bm7": ["B2", "D3", "F#3", "A3"],
    }
    
    # Extract the root notes for each chord
    root_notes = []
    for chord in chords:
        # Handle complex chord names by extracting just the root
        root = chord.split('m')[0].split('maj')[0].split('dim')[0].split('aug')[0].split('7')[0].split('9')[0].split('11')[0].split('13')[0].split('sus')[0].split('add')[0]
        
        # Find the matching chord or default to a simple triad
        if chord in chord_notes:
            chord_note_options = chord_notes[chord]
        else:
            # Try to find a close match
            for chord_name in chord_notes:
                if chord.startswith(chord_name):
                    chord_note_options = chord_notes[chord_name]
                    break
            else:
                # Default to a major or minor triad based on the chord name
                if 'm' in chord and 'maj' not in chord:
                    chord_note_options = chord_notes.get(f"{root}m", ["C2", "Eb2", "G2"])  # Default to Cm if not found
                else:
                    chord_note_options = chord_notes.get(root, ["C2", "E2", "G2"])  # Default to C if not found
        
        # Add the root note
        root_notes.append(chord_note_options[0])
    
    # Define bassline patterns by style
    patterns = {
        "walking": {
            "description": "Walking bass with quarter notes",
            "note_count": 4,  # Notes per chord
            "pattern": "root-fifth-third-approach",
        },
        "funk": {
            "description": "Syncopated funk pattern with sixteenth notes",
            "note_count": 8,  # Notes per chord
            "pattern": "syncopated-root-octave",
        },
        "rock": {
            "description": "Steady eighth note rock pattern",
            "note_count": 4,  # Notes per chord
            "pattern": "root-fifth-root-third",
        },
        "latin": {
            "description": "Latin-inspired pattern with emphasis on the tumbao",
            "note_count": 4,  # Notes per chord
            "pattern": "tumbao",
        },
        "jazz": {
            "description": "Jazz-inspired pattern with chromatic approaches",
            "note_count": 4,  # Notes per chord
            "pattern": "chromatic-approaches",
        },
        "pop": {
            "description": "Simple pop pattern focusing on roots and fifths",
            "note_count": 4,  # Notes per chord
            "pattern": "root-based",
        },
    }
    
    # Default to rock if style not found
    pattern_info = patterns.get(style.lower(), patterns["rock"])
    
    # Generate the bassline based on the style
    all_notes = []
    
    for i, chord in enumerate(chords):
        # Get the chord notes
        if chord in chord_notes:
            chord_note_options = chord_notes[chord]
        else:
            # Try to find a close match as before
            for chord_name in chord_notes:
                if chord.startswith(chord_name):
                    chord_note_options = chord_notes[chord_name]
                    break
            else:
                # Default based on chord type
                root = chord.split('m')[0].split('maj')[0].split('7')[0]
                if 'm' in chord and 'maj' not in chord:
                    chord_note_options = chord_notes.get(f"{root}m", ["C2", "Eb2", "G2"])
                else:
                    chord_note_options = chord_notes.get(root, ["C2", "E2", "G2"])
        
        # Get the next chord's root for approach notes
        next_chord_root = root_notes[(i + 1) % len(root_notes)]
        
        # Generate notes based on the style pattern
        chord_notes_list = []
        
        if pattern_info["pattern"] == "walking":
            # Walking bass: root, fifth, third, approach to next root
            root = chord_note_options[0]
            fifth = chord_note_options[2]  # Actually the fifth of the chord
            third = chord_note_options[1]  # Actually the third of the chord
            
            # Determine approach note to the next chord
            next_root_pitch = note_to_pitch(next_chord_root)
            current_root_pitch = note_to_pitch(root)
            
            if abs(next_root_pitch - current_root_pitch) <= 2:
                # Chromatic approach
                if next_root_pitch > current_root_pitch:
                    approach = pitch_to_note(next_root_pitch - 1)
                else:
                    approach = pitch_to_note(next_root_pitch + 1)
            else:
                # Scale approach
                if next_root_pitch > current_root_pitch:
                    approach = pitch_to_note(next_root_pitch - 2)
                else:
                    approach = pitch_to_note(next_root_pitch + 2)
            
            chord_notes_list = [root, fifth, third, approach]
            
        elif pattern_info["pattern"] == "syncopated-root-octave":
            # Funk: Syncopated pattern with root and octave
            root = chord_note_options[0]
            root_pitch = note_to_pitch(root)
            octave_up = pitch_to_note(root_pitch + 12)
            fifth = chord_note_options[2]
            
            # Create a syncopated pattern
            chord_notes_list = [
                root, "", octave_up, "",
                fifth, "", root, ""
            ]
            
            # Add some random variations
            for i in range(len(chord_notes_list)):
                if chord_notes_list[i] == "" and random.random() < 0.3:
                    # 30% chance to add a ghost note
                    if random.random() < 0.5:
                        chord_notes_list[i] = root
                    else:
                        chord_notes_list[i] = fifth
            
        elif pattern_info["pattern"] == "root-fifth-root-third":
            # Rock: Root-fifth-root-third pattern
            root = chord_note_options[0]
            fifth = chord_note_options[2]
            third = chord_note_options[1]
            
            chord_notes_list = [root, fifth, root, third]
            
        elif pattern_info["pattern"] == "tumbao":
            # Latin: Tumbao pattern
            root = chord_note_options[0]
            fifth = chord_note_options[2]
            
            # Basic tumbao pattern
            chord_notes_list = [root, "", fifth, "",
                               root, fifth, "", root]
            
        elif pattern_info["pattern"] == "chromatic-approaches":
            # Jazz: Chromatic approach pattern
            root = chord_note_options[0]
            third = chord_note_options[1]
            fifth = chord_note_options[2]
            
            # Get chromatic approach notes
            root_pitch = note_to_pitch(root)
            approach_below = pitch_to_note(root_pitch - 1)
            approach_above = pitch_to_note(root_pitch + 1)
            
            chord_notes_list = [root, third, fifth, approach_below]
            
            # Add some variation
            if random.random() < 0.5:
                chord_notes_list[3] = approach_above
            
        elif pattern_info["pattern"] == "root-based":
            # Pop: Simple root-based pattern
            root = chord_note_options[0]
            fifth = chord_note_options[2]
            
            chord_notes_list = [root, root, fifth, root]
        
        else:
            # Default pattern
            chord_notes_list = [chord_note_options[0]] * pattern_info["note_count"]
        
        # Add the notes for this chord to the overall bassline
        all_notes.extend([note for note in chord_notes_list if note])
    
    return all_notes, pattern_info["description"]


def note_to_pitch(note: str) -> int:
    """
    Convert a note name to a numeric pitch value.
    
    Args:
        note: Note name with octave (e.g., "C2")
        
    Returns:
        Integer pitch value
    """
    # Extract the note name and octave
    if len(note) >= 2:
        note_name = note[:-1]
        octave = int(note[-1])
    else:
        note_name = note
        octave = 4  # Default octave
    
    # Define the pitch values for each note
    note_values = {
        "C": 0, "C#": 1, "Db": 1,
        "D": 2, "D#": 3, "Eb": 3,
        "E": 4, "E#": 5, "Fb": 4,
        "F": 5, "F#": 6, "Gb": 6,
        "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10,
        "B": 11, "B#": 0, "Cb": 11
    }
    
    # Calculate the pitch value
    if note_name in note_values:
        return (octave + 1) * 12 + note_values[note_name]
    else:
        # Default to C4 if note not recognized
        return 60  # C4 in MIDI


def pitch_to_note(pitch: int) -> str:
    """
    Convert a numeric pitch value to a note name.
    
    Args:
        pitch: Integer pitch value
        
    Returns:
        Note name with octave (e.g., "C2")
    """
    # Define the note names
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    # Calculate the octave and note
    octave = (pitch // 12) - 1
    note_index = pitch % 12
    
    # Return the note name with octave
    return f"{note_names[note_index]}{octave}" 