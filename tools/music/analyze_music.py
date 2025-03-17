import random
from typing import Dict, Any, List


def analyze_music(args: dict) -> dict:
    """
    Analyzes music to extract key features like tempo, key, chord progression, and structure.
    
    Args:
        args: Dictionary containing the following keys:
            - audio_url: URL to the audio file to analyze
            - analysis_depth: Optional depth of analysis (default: 'detailed')
            
    Returns:
        Dictionary containing the analysis information
    """
    audio_url = args.get("audio_url", "")
    analysis_depth = args.get("analysis_depth", "detailed")
    
    # Validate inputs
    if not audio_url:
        return {
            "success": False,
            "error": "No audio URL provided"
        }
    
    # Generate analysis based on the depth
    analysis_data = generate_analysis(audio_url, analysis_depth)
    
    # Create an analysis description
    analysis_description = f"Performed a {analysis_depth} analysis of the audio"
    
    return {
        "success": True,
        "analysis_description": analysis_description,
        "audio_url": audio_url,
        "analysis_depth": analysis_depth,
        "tempo": analysis_data["tempo"],
        "key": analysis_data["key"],
        "time_signature": analysis_data["time_signature"],
        "chord_progression": analysis_data["chord_progression"],
        "structure": analysis_data["structure"],
        "instrumentation": analysis_data["instrumentation"],
        "spectral_analysis": analysis_data["spectral_analysis"],
        "dynamics": analysis_data["dynamics"],
        "genre_prediction": analysis_data["genre_prediction"],
        "mood_prediction": analysis_data["mood_prediction"],
        "similar_tracks": analysis_data.get("similar_tracks", [])
    }


def generate_analysis(audio_url: str, analysis_depth: str) -> Dict[str, Any]:
    """
    Generate analysis data based on the specified depth.
    
    Args:
        audio_url: URL to the audio file
        analysis_depth: Depth of analysis
        
    Returns:
        Dictionary containing analysis data
    """
    # Extract a unique identifier from the audio URL to use as a seed
    audio_id = audio_url.split("/")[-1].split(".")[0]
    
    # Use the audio ID to seed the random number generator for consistent results
    random.seed(audio_id)
    
    # Generate tempo (between 60 and 180 BPM)
    tempo = random.randint(60, 180)
    
    # Generate key
    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    modes = ["major", "minor"]
    key = f"{random.choice(keys)} {random.choice(modes)}"
    
    # Generate time signature
    time_signatures = ["4/4", "3/4", "6/8", "5/4", "7/8"]
    time_signature = random.choice(time_signatures)
    
    # Generate chord progression
    chord_progressions = {
        "C major": ["C", "G", "Am", "F"],
        "G major": ["G", "D", "Em", "C"],
        "D major": ["D", "A", "Bm", "G"],
        "A major": ["A", "E", "F#m", "D"],
        "E major": ["E", "B", "C#m", "A"],
        "F major": ["F", "C", "Dm", "Bb"],
        "Bb major": ["Bb", "F", "Gm", "Eb"],
        "Eb major": ["Eb", "Bb", "Cm", "Ab"],
        "Ab major": ["Ab", "Eb", "Fm", "Db"],
        "A minor": ["Am", "Em", "F", "G"],
        "E minor": ["Em", "Bm", "C", "D"],
        "D minor": ["Dm", "Am", "Bb", "C"],
        "G minor": ["Gm", "Dm", "Eb", "F"],
        "C minor": ["Cm", "Gm", "Ab", "Bb"],
    }
    
    # Choose a chord progression based on the key
    key_name = key.split()[0] + " " + key.split()[1]
    if key_name in chord_progressions:
        chord_progression = chord_progressions[key_name]
    else:
        # Default to C major if key not found
        chord_progression = chord_progressions["C major"]
    
    # Generate structure
    structures = [
        ["intro", "verse", "chorus", "verse", "chorus", "bridge", "chorus", "outro"],
        ["intro", "verse", "pre-chorus", "chorus", "verse", "pre-chorus", "chorus", "bridge", "chorus", "outro"],
        ["intro", "verse", "chorus", "verse", "chorus", "outro"],
        ["intro", "verse", "verse", "chorus", "verse", "chorus", "outro"],
        ["intro", "verse", "chorus", "verse", "chorus", "bridge", "verse", "chorus", "chorus", "outro"],
    ]
    structure = random.choice(structures)
    
    # Generate instrumentation
    instrument_categories = {
        "drums": ["acoustic drums", "electronic drums", "drum machine", "percussion"],
        "bass": ["electric bass", "synth bass", "upright bass", "bass guitar"],
        "harmony": ["piano", "guitar", "synthesizer", "organ", "strings"],
        "melody": ["vocals", "lead guitar", "synthesizer", "saxophone", "trumpet"],
        "effects": ["reverb", "delay", "distortion", "chorus", "flanger"]
    }
    
    # Select instruments from each category
    instrumentation = []
    for category, instruments in instrument_categories.items():
        # Add 1-2 instruments from each category
        num_instruments = random.randint(1, 2)
        selected_instruments = random.sample(instruments, min(num_instruments, len(instruments)))
        instrumentation.extend(selected_instruments)
    
    # Generate spectral analysis
    spectral_analysis = {
        "frequency_distribution": random.choice([
            "Balanced across the spectrum",
            "Emphasis on low frequencies",
            "Emphasis on mid-range frequencies",
            "Emphasis on high frequencies",
            "Strong bass and treble with recessed mids",
            "Warm with rolled-off highs",
            "Bright with emphasized highs"
        ]),
        "spectral_centroid": f"{random.uniform(500, 5000):.1f} Hz",
        "spectral_rolloff": f"{random.uniform(2000, 15000):.1f} Hz",
        "spectral_flatness": f"{random.uniform(0.01, 0.5):.3f}",
        "visualization_url": f"/analysis/spectrum/{audio_url.split('/')[-1].split('.')[0]}.png"
    }
    
    # Generate dynamics analysis
    dynamics = {
        "dynamic_range": f"{random.uniform(3, 20):.1f} dB",
        "peak_level": f"{-random.uniform(0.1, 3):.1f} dB",
        "rms_level": f"{-random.uniform(6, 20):.1f} dB",
        "crest_factor": f"{random.uniform(3, 15):.1f} dB",
        "loudness": f"{-random.uniform(5, 30):.1f} LUFS"
    }
    
    # Generate genre prediction
    genres = ["Pop", "Rock", "Electronic", "Hip-Hop", "R&B", "Jazz", "Classical", "Folk", "Country", "Metal"]
    genre_probabilities = {}
    
    # Generate random probabilities for each genre
    total_prob = 0
    for genre in genres:
        prob = random.uniform(0, 1)
        genre_probabilities[genre] = prob
        total_prob += prob
    
    # Normalize probabilities to sum to 1
    for genre in genre_probabilities:
        genre_probabilities[genre] /= total_prob
    
    # Sort genres by probability (descending)
    sorted_genres = sorted(genre_probabilities.items(), key=lambda x: x[1], reverse=True)
    
    # Format genre predictions
    genre_prediction = [{"genre": genre, "probability": f"{prob:.2f}"} for genre, prob in sorted_genres]
    
    # Generate mood prediction
    moods = ["Happy", "Sad", "Energetic", "Calm", "Aggressive", "Melancholic", "Romantic", "Tense", "Relaxed", "Nostalgic"]
    mood_probabilities = {}
    
    # Generate random probabilities for each mood
    total_prob = 0
    for mood in moods:
        prob = random.uniform(0, 1)
        mood_probabilities[mood] = prob
        total_prob += prob
    
    # Normalize probabilities to sum to 1
    for mood in mood_probabilities:
        mood_probabilities[mood] /= total_prob
    
    # Sort moods by probability (descending)
    sorted_moods = sorted(mood_probabilities.items(), key=lambda x: x[1], reverse=True)
    
    # Format mood predictions
    mood_prediction = [{"mood": mood, "probability": f"{prob:.2f}"} for mood, prob in sorted_moods]
    
    # Generate similar tracks (only for detailed analysis)
    similar_tracks = []
    if analysis_depth.lower() == "detailed":
        # Generate 3-5 similar tracks
        num_tracks = random.randint(3, 5)
        
        # Track names and artists
        track_names = [
            "Sunset Dreams", "Midnight Journey", "Electric Pulse", "Ocean Waves", 
            "Mountain Echo", "City Lights", "Desert Wind", "Forest Whispers", 
            "River Flow", "Starlight", "Neon Glow", "Cosmic Journey"
        ]
        
        artists = [
            "Harmony Project", "Rhythm Collective", "Sonic Wave", "Melody Masters", 
            "Beat Makers", "Sound Explorers", "Frequency", "Waveform", 
            "Echo Chamber", "Pulse", "Resonance", "Vibration"
        ]
        
        for _ in range(num_tracks):
            track = {
                "title": random.choice(track_names),
                "artist": random.choice(artists),
                "similarity_score": f"{random.uniform(0.7, 0.95):.2f}",
                "key": f"{random.choice(keys)} {random.choice(modes)}",
                "tempo": f"{random.randint(tempo-10, tempo+10)} BPM"
            }
            similar_tracks.append(track)
    
    # Compile the analysis data
    analysis_data = {
        "tempo": f"{tempo} BPM",
        "key": key,
        "time_signature": time_signature,
        "chord_progression": chord_progression,
        "structure": structure,
        "instrumentation": instrumentation,
        "spectral_analysis": spectral_analysis,
        "dynamics": dynamics,
        "genre_prediction": genre_prediction,
        "mood_prediction": mood_prediction,
        "similar_tracks": similar_tracks
    }
    
    return analysis_data 