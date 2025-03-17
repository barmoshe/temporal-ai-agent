import random
from typing import Dict, Any, List


def recommend_samples(args: dict) -> dict:
    """
    Recommends audio samples and loops that would fit with the current project.
    
    Args:
        args: Dictionary containing the following keys:
            - genre: Musical genre
            - tempo: Tempo in BPM
            - key: Optional musical key
            - instrument_types: Optional comma-separated list of instrument types to include
            
    Returns:
        Dictionary containing the recommended samples information
    """
    genre = args.get("genre", "electronic")
    tempo = int(args.get("tempo", 120))
    key = args.get("key", "")
    instrument_types_str = args.get("instrument_types", "drums,bass,synth")
    
    # Parse the instrument types
    instrument_types = [i.strip() for i in instrument_types_str.split(",") if i.strip()]
    
    # Generate sample recommendations
    recommendations = generate_sample_recommendations(genre, tempo, key, instrument_types)
    
    # Create a recommendation description
    if key:
        recommendation_description = f"Recommended {len(recommendations)} samples for {genre} at {tempo} BPM in {key}"
    else:
        recommendation_description = f"Recommended {len(recommendations)} samples for {genre} at {tempo} BPM"
    
    return {
        "success": True,
        "recommendation_description": recommendation_description,
        "genre": genre,
        "tempo": tempo,
        "key": key,
        "instrument_types": instrument_types,
        "recommendations": recommendations
    }


def generate_sample_recommendations(genre: str, tempo: int, key: str, instrument_types: List[str]) -> List[Dict[str, Any]]:
    """
    Generate a list of recommended samples based on the specified parameters.
    
    Args:
        genre: Musical genre
        tempo: Tempo in BPM
        key: Musical key (optional)
        instrument_types: List of instrument types to include
        
    Returns:
        List of sample recommendation objects
    """
    # Define sample libraries by genre
    sample_libraries = {
        "electronic": [
            "Deep House Essentials",
            "Tech House Toolkit",
            "EDM Drops",
            "Analog Synth Collection",
            "Future Bass Elements",
            "Techno Percussion",
            "Ambient Textures",
            "Drum & Bass Breaks",
            "Dubstep Wobbles",
            "Trance Arpeggios"
        ],
        "hip-hop": [
            "Boom Bap Drums",
            "Trap 808s",
            "Lo-Fi Samples",
            "Hip-Hop Vinyl Cuts",
            "Urban Vocal Chops",
            "Dirty South Drums",
            "East Coast Samples",
            "West Coast G-Funk",
            "Drill Percussion",
            "Rap Acapellas"
        ],
        "rock": [
            "Classic Rock Drums",
            "Guitar Riffs",
            "Bass Grooves",
            "Indie Rock Elements",
            "Alternative Percussion",
            "Rock Vocal Samples",
            "Distorted Guitars",
            "Live Drum Loops",
            "Rock Organ Samples",
            "Punk Drum Fills"
        ],
        "jazz": [
            "Jazz Drum Loops",
            "Upright Bass Samples",
            "Piano Jazz Chords",
            "Saxophone Riffs",
            "Trumpet Licks",
            "Brushed Drums",
            "Jazz Guitar Comping",
            "Vibraphone Samples",
            "Double Bass Loops",
            "Jazz Ensemble Hits"
        ],
        "pop": [
            "Modern Pop Drums",
            "Vocal Chops",
            "Pop Synth Leads",
            "Chart Toppers Percussion",
            "Pop Piano Chords",
            "Radio Ready Drums",
            "Pop Vocal Adlibs",
            "Contemporary Bass Loops",
            "Pop Guitar Loops",
            "Commercial Drum Fills"
        ],
        "classical": [
            "Orchestral Strings",
            "Classical Piano",
            "Symphonic Percussion",
            "Woodwind Ensembles",
            "Brass Sections",
            "Chamber Strings",
            "Harp Glissandos",
            "Timpani Rolls",
            "Choir Samples",
            "Orchestral Hits"
        ],
        "world": [
            "African Percussion",
            "Indian Tabla Loops",
            "Latin Percussion",
            "Middle Eastern Oud",
            "Asian String Instruments",
            "Celtic Harp",
            "Balkan Brass",
            "Reggae Skank Guitars",
            "Afrobeat Percussion",
            "Flamenco Guitar"
        ],
        "ambient": [
            "Atmospheric Pads",
            "Cinematic Textures",
            "Field Recordings",
            "Drone Sounds",
            "Evolving Soundscapes",
            "Granular Textures",
            "Ambient Piano",
            "Ethereal Vocals",
            "Processed Nature Sounds",
            "Ambient Guitar Loops"
        ]
    }
    
    # Define instrument types and their variations
    instrument_variations = {
        "drums": [
            "Kick", "Snare", "Hi-Hat", "Clap", "Percussion", "Tom", "Cymbal", 
            "Drum Loop", "Drum Fill", "Drum Break", "Drum Kit", "Drum One-Shot"
        ],
        "bass": [
            "Bass Loop", "808", "Sub Bass", "Bass One-Shot", "Bass Line", 
            "Synth Bass", "Electric Bass", "Upright Bass", "Acoustic Bass"
        ],
        "synth": [
            "Synth Lead", "Synth Pad", "Synth Arpeggio", "Synth Pluck", 
            "Synth Chord", "Synth Texture", "Synth FX", "Synth Sequence"
        ],
        "piano": [
            "Piano Loop", "Piano Chord", "Piano Melody", "Piano Arpeggio", 
            "Electric Piano", "Upright Piano", "Grand Piano", "Piano FX"
        ],
        "guitar": [
            "Guitar Loop", "Guitar Riff", "Guitar Chord", "Acoustic Guitar", 
            "Electric Guitar", "Guitar Lick", "Guitar Strum", "Guitar FX"
        ],
        "strings": [
            "String Ensemble", "Violin", "Cello", "Viola", "Double Bass", 
            "String Loop", "String Pad", "Pizzicato Strings", "String FX"
        ],
        "brass": [
            "Brass Section", "Trumpet", "Trombone", "Saxophone", "Horn", 
            "Brass Stab", "Brass Loop", "Brass FX"
        ],
        "vocals": [
            "Vocal Loop", "Vocal Chop", "Vocal Phrase", "Vocal One-Shot", 
            "Vocal FX", "Vocal Adlib", "Acapella", "Vocal Sample"
        ],
        "fx": [
            "Riser", "Downlifter", "Impact", "Transition", "Sweep", "Glitch", 
            "Noise", "Atmosphere", "Foley", "Sound Design"
        ]
    }
    
    # Default to electronic if genre not found
    library = sample_libraries.get(genre.lower(), sample_libraries["electronic"])
    
    # Generate recommendations
    recommendations = []
    
    # Number of recommendations to generate (5-15)
    num_recommendations = random.randint(5, 15)
    
    for _ in range(num_recommendations):
        # Choose a random instrument type from the requested types
        if instrument_types:
            instrument_type = random.choice(instrument_types)
        else:
            instrument_type = random.choice(list(instrument_variations.keys()))
        
        # Get variations for this instrument type
        variations = instrument_variations.get(instrument_type, ["Sample"])
        
        # Choose a random variation
        variation = random.choice(variations)
        
        # Choose a random library
        sample_library = random.choice(library)
        
        # Generate a sample name
        sample_name = f"{sample_library} - {variation}"
        
        # Generate a sample tempo (within ±5 BPM of the requested tempo)
        sample_tempo = tempo + random.randint(-5, 5)
        sample_tempo = max(60, min(200, sample_tempo))  # Keep within reasonable range
        
        # Generate a sample key if requested
        sample_key = ""
        if key:
            # 80% chance to match the requested key, 20% chance for a related key
            if random.random() < 0.8:
                sample_key = key
            else:
                # Generate a related key
                related_keys = generate_related_keys(key)
                sample_key = random.choice(related_keys)
        
        # Generate a preview URL
        preview_url = f"/samples/{genre.lower()}/{instrument_type.lower()}/{variation.lower().replace(' ', '_')}_{random.randint(1000, 9999)}.mp3"
        
        # Add the recommendation
        recommendation = {
            "name": sample_name,
            "type": instrument_type,
            "subtype": variation,
            "tempo": sample_tempo,
            "preview_url": preview_url,
            "library": sample_library,
            "tags": [genre, instrument_type, variation.split()[0].lower()]
        }
        
        # Add key if available
        if sample_key:
            recommendation["key"] = sample_key
        
        # Add some random attributes based on the instrument type
        if instrument_type == "drums":
            recommendation["loop_length"] = f"{random.choice([1, 2, 4, 8])} bars"
        elif instrument_type == "bass":
            recommendation["note_range"] = f"{random.choice(['C1', 'D1', 'E1', 'F1', 'G1'])} - {random.choice(['C3', 'D3', 'E3', 'F3', 'G3'])}"
        elif instrument_type == "synth":
            recommendation["character"] = random.choice(["Bright", "Dark", "Warm", "Cold", "Aggressive", "Smooth", "Distorted", "Clean"])
        
        recommendations.append(recommendation)
    
    return recommendations


def generate_related_keys(key: str) -> List[str]:
    """
    Generate a list of musically related keys.
    
    Args:
        key: The original key
        
    Returns:
        List of related keys
    """
    # Define key relationships
    key_relationships = {
        "C": ["Am", "F", "G"],
        "C#": ["A#m", "F#", "G#"],
        "Db": ["Bbm", "Gb", "Ab"],
        "D": ["Bm", "G", "A"],
        "D#": ["Cm", "G#", "A#"],
        "Eb": ["Cm", "Ab", "Bb"],
        "E": ["C#m", "A", "B"],
        "F": ["Dm", "Bb", "C"],
        "F#": ["D#m", "B", "C#"],
        "Gb": ["Ebm", "Cb", "Db"],
        "G": ["Em", "C", "D"],
        "G#": ["Fm", "C#", "D#"],
        "Ab": ["Fm", "Db", "Eb"],
        "A": ["F#m", "D", "E"],
        "A#": ["Gm", "D#", "F"],
        "Bb": ["Gm", "Eb", "F"],
        "B": ["G#m", "E", "F#"],
        
        "Am": ["C", "Dm", "Em"],
        "A#m": ["C#", "D#m", "Fm"],
        "Bbm": ["Db", "Ebm", "Fm"],
        "Bm": ["D", "Em", "F#m"],
        "Cm": ["Eb", "Fm", "Gm"],
        "C#m": ["E", "F#m", "G#m"],
        "Dm": ["F", "Gm", "Am"],
        "D#m": ["F#", "G#m", "A#m"],
        "Ebm": ["Gb", "Abm", "Bbm"],
        "Em": ["G", "Am", "Bm"],
        "Fm": ["Ab", "Bbm", "Cm"],
        "F#m": ["A", "Bm", "C#m"],
        "Gm": ["Bb", "Cm", "Dm"],
        "G#m": ["B", "C#m", "D#m"],
        "Abm": ["Cb", "Dbm", "Ebm"],
    }
    
    # Return related keys or default to a few common keys
    return key_relationships.get(key, ["C", "Am", "G", "Em"]) 