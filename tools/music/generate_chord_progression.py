import random
from typing import Dict, Any, List


def generate_chord_progression(args: dict) -> dict:
    """
    Generates a chord progression based on specified parameters.
    
    Args:
        args: Dictionary containing the following keys:
            - key: Musical key (e.g., 'C', 'F#', 'Bb')
            - style: Musical style (e.g., 'pop', 'jazz', 'classical')
            - length: Optional number of chords (default: 4)
            - complexity: Optional complexity level (default: 'moderate')
            
    Returns:
        Dictionary containing the generated chord progression information
    """
    key = args.get("key", "C")
    style = args.get("style", "pop")
    length = int(args.get("length", 4))
    complexity = args.get("complexity", "moderate")
    
    # Generate a chord progression based on the parameters
    chords, roman_numerals = generate_chord_sequence(key, style, length, complexity)
    
    # Create a chord progression description
    progression_description = f"Generated a {length}-chord {complexity} {style} progression in {key}"
    
    # Format the progression as a string
    progression_notation = " - ".join(chords)
    
    # Generate a mock visualization URL
    visualization_url = f"/compositions/chord_charts/{key.replace('#', 'sharp').replace('b', 'flat')}_{style}_{complexity}.png"
    
    return {
        "success": True,
        "progression_description": progression_description,
        "chords": chords,
        "roman_numerals": roman_numerals,
        "notation": progression_notation,
        "key": key,
        "style": style,
        "complexity": complexity,
        "visualization_url": visualization_url
    }


def generate_chord_sequence(key: str, style: str, length: int, complexity: str) -> tuple:
    """
    Generate a sequence of chords based on music theory and the specified style.
    
    Args:
        key: The musical key
        style: The musical style
        length: Number of chords
        complexity: Complexity level
        
    Returns:
        Tuple of (chord_names, roman_numerals)
    """
    # Define the chords for each key
    major_keys = {
        "C": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
        "C#": ["C#", "D#m", "E#m", "F#", "G#", "A#m", "B#dim"],
        "Db": ["Db", "Ebm", "Fm", "Gb", "Ab", "Bbm", "Cdim"],
        "D": ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
        "D#": ["D#", "E#m", "F##m", "G#", "A#", "B#m", "C##dim"],
        "Eb": ["Eb", "Fm", "Gm", "Ab", "Bb", "Cm", "Ddim"],
        "E": ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
        "F": ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"],
        "F#": ["F#", "G#m", "A#m", "B", "C#", "D#m", "E#dim"],
        "Gb": ["Gb", "Abm", "Bbm", "Cb", "Db", "Ebm", "Fdim"],
        "G": ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
        "G#": ["G#", "A#m", "B#m", "C#", "D#", "E#m", "F##dim"],
        "Ab": ["Ab", "Bbm", "Cm", "Db", "Eb", "Fm", "Gdim"],
        "A": ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
        "A#": ["A#", "B#m", "C##m", "D#", "E#", "F##m", "G##dim"],
        "Bb": ["Bb", "Cm", "Dm", "Eb", "F", "Gm", "Adim"],
        "B": ["B", "C#m", "D#m", "E", "F#", "G#m", "A#dim"],
    }
    
    minor_keys = {
        "Cm": ["Cm", "Ddim", "Eb", "Fm", "Gm", "Ab", "Bb"],
        "C#m": ["C#m", "D#dim", "E", "F#m", "G#m", "A", "B"],
        "Dm": ["Dm", "Edim", "F", "Gm", "Am", "Bb", "C"],
        "D#m": ["D#m", "E#dim", "F#", "G#m", "A#m", "B", "C#"],
        "Ebm": ["Ebm", "Fdim", "Gb", "Abm", "Bbm", "Cb", "Db"],
        "Em": ["Em", "F#dim", "G", "Am", "Bm", "C", "D"],
        "Fm": ["Fm", "Gdim", "Ab", "Bbm", "Cm", "Db", "Eb"],
        "F#m": ["F#m", "G#dim", "A", "Bm", "C#m", "D", "E"],
        "Gm": ["Gm", "Adim", "Bb", "Cm", "Dm", "Eb", "F"],
        "G#m": ["G#m", "A#dim", "B", "C#m", "D#m", "E", "F#"],
        "Abm": ["Abm", "Bbdim", "Cb", "Dbm", "Ebm", "Fb", "Gb"],
        "Am": ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
        "A#m": ["A#m", "B#dim", "C#", "D#m", "E#m", "F#", "G#"],
        "Bbm": ["Bbm", "Cdim", "Db", "Ebm", "Fm", "Gb", "Ab"],
        "Bm": ["Bm", "C#dim", "D", "Em", "F#m", "G", "A"],
    }
    
    # Roman numeral representations
    major_numerals = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
    minor_numerals = ["i", "ii°", "III", "iv", "v", "VI", "VII"]
    
    # Determine if the key is minor
    is_minor = key.endswith('m') or key.endswith('min')
    
    # Get the appropriate key chords
    if is_minor:
        # Handle the case where the key might be specified as "Cmin" or similar
        clean_key = key.replace('min', 'm')
        key_chords = minor_keys.get(clean_key, minor_keys.get("Am"))
        numerals = minor_numerals
    else:
        key_chords = major_keys.get(key, major_keys.get("C"))
        numerals = major_numerals
    
    # Define common chord progressions by style
    progressions = {
        "pop": {
            "simple": [
                [0, 3, 4, 0],  # I-IV-V-I
                [0, 3, 5, 4],  # I-IV-vi-V
                [0, 5, 3, 4],  # I-vi-IV-V
                [5, 3, 0, 4],  # vi-IV-I-V
            ],
            "moderate": [
                [0, 5, 3, 4, 0],  # I-vi-IV-V-I
                [0, 3, 4, 5, 0],  # I-IV-V-vi-I
                [0, 5, 1, 4, 0],  # I-vi-ii-V-I
                [0, 3, 5, 1, 4],  # I-IV-vi-ii-V
            ],
            "complex": [
                [0, 5, 1, 2, 3, 4],  # I-vi-ii-iii-IV-V
                [0, 3, 5, 1, 2, 4],  # I-IV-vi-ii-iii-V
                [0, 5, 3, 4, 1, 2],  # I-vi-IV-V-ii-iii
                [0, 2, 5, 1, 3, 4],  # I-iii-vi-ii-IV-V
            ],
        },
        "jazz": {
            "simple": [
                [1, 4, 0, 4],  # ii-V-I-V
                [1, 4, 0, 3],  # ii-V-I-IV
                [0, 3, 1, 4],  # I-IV-ii-V
                [0, 5, 1, 4],  # I-vi-ii-V
            ],
            "moderate": [
                [1, 4, 0, 5, 1, 4],  # ii-V-I-vi-ii-V
                [0, 5, 1, 4, 0, 3],  # I-vi-ii-V-I-IV
                [1, 4, 0, 3, 5, 1],  # ii-V-I-IV-vi-ii
                [0, 2, 5, 1, 4, 0],  # I-iii-vi-ii-V-I
            ],
            "complex": [
                [1, 4, 0, 3, 5, 1, 2, 4],  # ii-V-I-IV-vi-ii-iii-V
                [0, 5, 1, 4, 0, 3, 5, 1],  # I-vi-ii-V-I-IV-vi-ii
                [0, 2, 5, 1, 4, 0, 3, 5],  # I-iii-vi-ii-V-I-IV-vi
                [1, 4, 0, 6, 2, 5, 1, 4],  # ii-V-I-vii-iii-vi-ii-V
            ],
        },
        "classical": {
            "simple": [
                [0, 4, 0, 4],  # I-V-I-V
                [0, 4, 5, 0],  # I-V-vi-I
                [0, 3, 4, 0],  # I-IV-V-I
                [0, 1, 4, 0],  # I-ii-V-I
            ],
            "moderate": [
                [0, 4, 5, 3, 4, 0],  # I-V-vi-IV-V-I
                [0, 1, 4, 5, 4, 0],  # I-ii-V-vi-V-I
                [0, 3, 1, 4, 0, 4],  # I-IV-ii-V-I-V
                [0, 5, 3, 1, 4, 0],  # I-vi-IV-ii-V-I
            ],
            "complex": [
                [0, 5, 2, 3, 1, 4, 0],  # I-vi-iii-IV-ii-V-I
                [0, 3, 5, 1, 2, 4, 0],  # I-IV-vi-ii-iii-V-I
                [0, 2, 5, 3, 1, 4, 0],  # I-iii-vi-IV-ii-V-I
                [0, 4, 2, 5, 1, 3, 4, 0],  # I-V-iii-vi-ii-IV-V-I
            ],
        },
        "rock": {
            "simple": [
                [0, 4, 5, 4],  # I-V-vi-V
                [0, 3, 4, 3],  # I-IV-V-IV
                [0, 5, 3, 4],  # I-vi-IV-V
                [0, 4, 0, 3],  # I-V-I-IV
            ],
            "moderate": [
                [0, 3, 5, 4, 0],  # I-IV-vi-V-I
                [0, 5, 3, 4, 0],  # I-vi-IV-V-I
                [0, 4, 5, 3, 0],  # I-V-vi-IV-I
                [0, 3, 4, 5, 0],  # I-IV-V-vi-I
            ],
            "complex": [
                [0, 3, 5, 4, 0, 3, 4, 0],  # I-IV-vi-V-I-IV-V-I
                [0, 5, 3, 4, 0, 5, 3, 4],  # I-vi-IV-V-I-vi-IV-V
                [0, 3, 4, 0, 5, 3, 4, 0],  # I-IV-V-I-vi-IV-V-I
                [0, 5, 3, 4, 5, 3, 4, 0],  # I-vi-IV-V-vi-IV-V-I
            ],
        },
        "blues": {
            "simple": [
                [0, 0, 0, 0, 3, 3, 0, 0, 4, 3, 0, 4],  # I-I-I-I-IV-IV-I-I-V-IV-I-V (12-bar blues)
                [0, 3, 0, 4],  # I-IV-I-V
                [0, 0, 3, 3, 0, 0, 4, 3],  # I-I-IV-IV-I-I-V-IV (8-bar blues)
                [0, 3, 4, 3],  # I-IV-V-IV
            ],
            "moderate": [
                [0, 0, 0, 0, 3, 3, 0, 0, 4, 3, 0, 0],  # I-I-I-I-IV-IV-I-I-V-IV-I-I
                [0, 3, 0, 4, 3, 0, 4, 0],  # I-IV-I-V-IV-I-V-I
                [0, 0, 3, 3, 0, 4, 3, 0],  # I-I-IV-IV-I-V-IV-I
                [0, 3, 4, 3, 0, 4, 0, 3],  # I-IV-V-IV-I-V-I-IV
            ],
            "complex": [
                [0, 0, 0, 3, 3, 0, 0, 4, 3, 0, 4, 0],  # I-I-I-IV-IV-I-I-V-IV-I-V-I
                [0, 3, 0, 3, 0, 4, 3, 0, 4, 3, 0, 4],  # I-IV-I-IV-I-V-IV-I-V-IV-I-V
                [0, 0, 3, 3, 0, 0, 4, 4, 3, 3, 0, 0],  # I-I-IV-IV-I-I-V-V-IV-IV-I-I
                [0, 3, 4, 3, 0, 3, 4, 3, 0, 4, 3, 0],  # I-IV-V-IV-I-IV-V-IV-I-V-IV-I
            ],
        },
    }
    
    # Default to pop if style not found
    style_progressions = progressions.get(style.lower(), progressions["pop"])
    
    # Default to moderate if complexity not found
    complexity_progressions = style_progressions.get(complexity.lower(), style_progressions["moderate"])
    
    # Choose a progression
    progression_indices = random.choice(complexity_progressions)
    
    # If the requested length is different from the chosen progression, adjust
    if len(progression_indices) != length:
        if len(progression_indices) > length:
            # Truncate the progression
            progression_indices = progression_indices[:length]
        else:
            # Extend the progression by repeating elements
            while len(progression_indices) < length:
                progression_indices.append(progression_indices[len(progression_indices) % len(progression_indices)])
    
    # Convert indices to actual chords and numerals
    chords = [key_chords[idx] for idx in progression_indices]
    roman_nums = [numerals[idx] for idx in progression_indices]
    
    # Add extensions for jazz and more complex progressions
    if style.lower() == "jazz" or complexity.lower() == "complex":
        chords = add_chord_extensions(chords, style.lower(), complexity.lower())
    
    return chords, roman_nums


def add_chord_extensions(chords: List[str], style: str, complexity: str) -> List[str]:
    """
    Add extensions to chords based on style and complexity.
    
    Args:
        chords: List of basic chord names
        style: Musical style
        complexity: Complexity level
        
    Returns:
        List of chords with extensions
    """
    extended_chords = []
    
    for chord in chords:
        # Determine if the chord is major, minor, or diminished
        is_minor = "m" in chord and "maj" not in chord
        is_diminished = "dim" in chord
        
        # Basic extensions based on chord type
        if is_diminished:
            extensions = ["dim", "dim7", "m7b5"]
        elif is_minor:
            if style == "jazz":
                extensions = ["m7", "m9", "m11", "m6", "m6/9"]
            elif complexity == "complex":
                extensions = ["m7", "m9", "m6", "madd9"]
            else:
                extensions = ["m", "m7", "m6"]
        else:  # Major chord
            if style == "jazz":
                extensions = ["maj7", "maj9", "6", "6/9", "9", "13"]
            elif complexity == "complex":
                extensions = ["maj7", "add9", "6", "9"]
            else:
                extensions = ["", "7", "maj7"]
        
        # Choose an extension based on complexity
        if complexity == "simple":
            # For simple, prefer basic extensions
            weight = [0.7, 0.2, 0.1] + [0.0] * (len(extensions) - 3)
            extension = random.choices(extensions, weights=weight, k=1)[0]
        elif complexity == "moderate":
            # For moderate, use a mix
            weight = [0.4, 0.3, 0.2, 0.1] + [0.0] * (len(extensions) - 4)
            extension = random.choices(extensions, weights=weight, k=1)[0]
        else:  # complex
            # For complex, prefer more interesting extensions
            weight = [0.1, 0.2, 0.3, 0.2, 0.2] + [0.0] * (len(extensions) - 5)
            extension = random.choices(extensions, weights=weight, k=1)[0]
        
        # Apply the extension
        if is_diminished:
            # For diminished chords, replace the "dim" part
            base_chord = chord.replace("dim", "")
            extended_chords.append(f"{base_chord}{extension}")
        elif is_minor:
            # For minor chords, keep the "m" and add the extension
            if extension == "m":
                extended_chords.append(chord)  # Already has "m"
            else:
                # Replace "m" with the extension if it starts with "m"
                if extension.startswith("m"):
                    base_chord = chord.replace("m", "")
                    extended_chords.append(f"{base_chord}{extension}")
                else:
                    extended_chords.append(f"{chord}{extension}")
        else:
            # For major chords, just add the extension
            extended_chords.append(f"{chord}{extension}")
    
    return extended_chords 