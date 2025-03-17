import random
from typing import Dict, Any, List


def generate_drum_pattern(args: dict) -> dict:
    """
    Generates a drum pattern based on specified style and tempo.
    
    Args:
        args: Dictionary containing the following keys:
            - style: Drum style (e.g., 'rock', 'hip-hop', 'jazz')
            - tempo: Tempo in BPM
            - complexity: Optional complexity level (default: 'moderate')
            - bars: Optional number of bars (default: 2)
            
    Returns:
        Dictionary containing the generated drum pattern information
    """
    style = args.get("style", "rock")
    tempo = int(args.get("tempo", 120))
    complexity = args.get("complexity", "moderate")
    bars = int(args.get("bars", 2))
    
    # Generate a drum pattern based on the parameters
    pattern, notation = generate_drum_sequence(style, complexity, bars)
    
    # Create a pattern description
    pattern_description = f"Generated a {bars}-bar {complexity} {style} drum pattern at {tempo} BPM"
    
    # Generate a mock MIDI file path
    midi_file = f"/compositions/drums/{style}_{complexity}_{tempo}bpm_{bars}bars.mid"
    
    # Generate a mock audio preview path
    audio_preview = f"/compositions/previews/drums_{style}_{tempo}bpm.mp3"
    
    # Generate a mock visualization path
    visualization = f"/compositions/visualizations/drums_{style}_{complexity}_{bars}bars.png"
    
    return {
        "success": True,
        "pattern_description": pattern_description,
        "pattern": pattern,
        "notation": notation,
        "style": style,
        "tempo": tempo,
        "complexity": complexity,
        "bars": bars,
        "midi_file": midi_file,
        "audio_preview": audio_preview,
        "visualization": visualization
    }


def generate_drum_sequence(style: str, complexity: str, bars: int) -> tuple:
    """
    Generate a drum pattern sequence based on the specified style and complexity.
    
    Args:
        style: The drum style
        complexity: Complexity level
        bars: Number of bars
        
    Returns:
        Tuple of (pattern_dict, notation_string)
    """
    # Define common drum patterns by style
    patterns = {
        "rock": {
            "simple": {
                "kick": "X...X...X...X...",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
                "crash": "X...............",
            },
            "moderate": {
                "kick": "X...X..XX...X...",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
                "crash": "X...............",
                "tom": "..........X.X...",
            },
            "complex": {
                "kick": "X...X..XX..XX.X.",
                "snare": "....X.X.....X.X.",
                "hi-hat": "X.XXX.X.X.XXX.X.",
                "crash": "X...............",
                "tom": "..........X.XXX.",
                "ride": ".....X.X........",
            },
        },
        "hip-hop": {
            "simple": {
                "kick": "X.....X.........",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
            },
            "moderate": {
                "kick": "X.....X...X.....",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
                "percussion": "..X...X...X...X.",
            },
            "complex": {
                "kick": "X..X..X...X.X...",
                "snare": "....X.X.....X.X.",
                "hi-hat": "X.XXX.X.X.XXX.X.",
                "percussion": "..X...X...X.X.X.",
                "open-hat": "........X.......",
            },
        },
        "jazz": {
            "simple": {
                "kick": "X.......X.......",
                "snare": "....X.......X...",
                "ride": "X.X.X.X.X.X.X.X.",
                "hi-hat": "....X.......X...",
            },
            "moderate": {
                "kick": "X.......X..X....",
                "snare": "....X.X.....X.X.",
                "ride": "X.X.X.X.X.X.X.X.",
                "hi-hat": "....X.......X...",
                "brush": "...X...X...X...X",
            },
            "complex": {
                "kick": "X.....X.X...X...",
                "snare": "..X.X...X.X...X.",
                "ride": "X.X.X.X.X.X.X.X.",
                "hi-hat": "....X.......X...",
                "brush": "...X...X...X...X",
                "crash": "........X.......",
            },
        },
        "electronic": {
            "simple": {
                "kick": "X...X...X...X...",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
                "clap": "....X.......X...",
            },
            "moderate": {
                "kick": "X...X..XX...X...",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
                "clap": "....X.......X...",
                "percussion": "..X...X...X...X.",
            },
            "complex": {
                "kick": "X..XX..XX..XX.X.",
                "snare": "....X.X.....X.X.",
                "hi-hat": "X.XXX.X.X.XXX.X.",
                "clap": "....X.......X...",
                "percussion": "..X.X.X...X.X.X.",
                "open-hat": "........X.......",
            },
        },
        "funk": {
            "simple": {
                "kick": "X...X...X...X...",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
            },
            "moderate": {
                "kick": "X.X...X.X...X.X.",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
                "percussion": "..X...X...X...X.",
            },
            "complex": {
                "kick": "X.X...X.X.X...X.",
                "snare": "....X.X...X.X...",
                "hi-hat": "X.XXX.X.X.XXX.X.",
                "percussion": "..X...X...X...X.",
                "open-hat": "........X.......",
                "tom": "............X.X.",
            },
        },
        "latin": {
            "simple": {
                "kick": "X.......X.......",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
                "conga": "..X...X...X...X.",
            },
            "moderate": {
                "kick": "X.......X.......",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
                "conga": "..X.X.X...X.X.X.",
                "cowbell": "X...X...X...X...",
            },
            "complex": {
                "kick": "X.......X.......",
                "snare": "....X.......X...",
                "hi-hat": "X.X.X.X.X.X.X.X.",
                "conga": "..X.X.X...X.X.X.",
                "cowbell": "X...X...X...X...",
                "timbale": "........X.X.X.X.",
                "shaker": "X.X.X.X.X.X.X.X.",
            },
        },
    }
    
    # Default to rock if style not found
    style_patterns = patterns.get(style.lower(), patterns["rock"])
    
    # Default to moderate if complexity not found
    complexity_pattern = style_patterns.get(complexity.lower(), style_patterns["moderate"])
    
    # Create the pattern dictionary
    pattern = {}
    
    # For each drum part, generate the pattern for the requested number of bars
    for drum, base_pattern in complexity_pattern.items():
        # Repeat the pattern for the requested number of bars
        full_pattern = base_pattern * bars
        
        # Add some variation for longer patterns
        if bars > 1 and complexity != "simple":
            # Convert to list for easier manipulation
            pattern_list = list(full_pattern)
            
            # Add variations at different points
            for bar in range(1, bars):
                # Calculate the start position of this bar
                start_pos = bar * len(base_pattern)
                
                # Add some random variations
                num_variations = 2 if complexity == "moderate" else 4
                for _ in range(num_variations):
                    pos = start_pos + random.randint(0, len(base_pattern) - 1)
                    if pos < len(pattern_list):
                        # Either add or remove a hit
                        if pattern_list[pos] == "X":
                            if random.random() < 0.3:  # 30% chance to remove
                                pattern_list[pos] = "."
                        else:
                            if random.random() < 0.2:  # 20% chance to add
                                pattern_list[pos] = "X"
            
            # Convert back to string
            full_pattern = "".join(pattern_list)
        
        pattern[drum] = full_pattern
    
    # Generate a text notation of the pattern
    notation = generate_drum_notation(pattern)
    
    return pattern, notation


def generate_drum_notation(pattern: Dict[str, str]) -> str:
    """
    Generate a text-based notation of the drum pattern.
    
    Args:
        pattern: Dictionary mapping drum parts to their patterns
        
    Returns:
        String representation of the drum pattern
    """
    # Order the drums in a standard way
    drum_order = [
        "crash", "ride", "open-hat", "hi-hat", 
        "snare", "kick", "tom", "percussion", 
        "conga", "cowbell", "timbale", "shaker", "brush", "clap"
    ]
    
    # Filter to only include drums that are in the pattern
    drums = [d for d in drum_order if d in pattern]
    
    # Build the notation
    notation = []
    
    # Add a header line showing beat numbers
    beats = len(list(pattern.values())[0]) // 4
    beat_numbers = "".join([f"{i+1}   " for i in range(beats)])
    notation.append(f"Beat: {beat_numbers}")
    
    # Add a line showing 16th notes
    sixteenths = "".join(["x . . . " for _ in range(beats)])
    notation.append(f"     {sixteenths}")
    
    # Add each drum part
    for drum in drums:
        # Convert the pattern to a more readable format
        readable = ""
        for i, char in enumerate(pattern[drum]):
            if i % 4 == 0:
                readable += " "
            readable += char + " "
        
        # Add the drum name and pattern
        notation.append(f"{drum.ljust(8)}{readable}")
    
    return "\n".join(notation) 