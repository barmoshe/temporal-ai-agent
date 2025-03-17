import random
import uuid
from datetime import datetime


def create_music_composition(args: dict) -> dict:
    """
    Create a custom music composition based on user preferences for genre, mood, tempo, and instruments.
    Returns details about the composition including title, genre, instruments used, duration, and a download link.
    """
    genre = args.get("genre", "").capitalize()
    mood = args.get("mood", "").lower()
    tempo = args.get("tempo", "").lower()
    instruments_str = args.get("instruments", "")
    
    # Parse instruments list
    instruments = [i.strip().capitalize() for i in instruments_str.split(",") if i.strip()]
    
    # Validate inputs
    if not all([genre, mood, tempo]) or not instruments:
        return {"error": "Missing required composition information"}
    
    # Generate a composition ID
    composition_id = f"COMP-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4]}"
    
    # Generate a title based on genre, mood, and instruments
    title = generate_composition_title(genre, mood, instruments)
    
    # Generate a random duration between 2 and 8 minutes
    minutes = random.randint(2, 7)
    seconds = random.randint(0, 59)
    duration = f"{minutes}:{seconds:02d}"
    
    # Generate a mock download URL
    download_url = f"https://example.com/compositions/{title.lower().replace(' ', '-')}.mp3"
    
    # Generate sample stems for each instrument
    stems = []
    for instrument in instruments:
        stems.append({
            "instrument": instrument,
            "download_url": f"https://example.com/compositions/stems/{title.lower().replace(' ', '-')}-{instrument.lower()}.wav"
        })
    
    return {
        "composition_id": composition_id,
        "title": title,
        "genre": genre,
        "mood": mood.capitalize(),
        "tempo": tempo.capitalize(),
        "instruments": instruments,
        "duration": duration,
        "download_url": download_url,
        "stems": stems,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def generate_composition_title(genre: str, mood: str, instruments: list) -> str:
    """Generate a creative title for the composition based on its attributes."""
    # Title components by mood
    mood_words = {
        "happy": ["Joy", "Celebration", "Sunshine", "Bliss", "Delight", "Euphoria", "Radiance"],
        "sad": ["Melancholy", "Sorrow", "Tears", "Nostalgia", "Longing", "Reflection", "Shadows"],
        "energetic": ["Pulse", "Surge", "Velocity", "Momentum", "Ignition", "Spark", "Dynamism"],
        "relaxed": ["Serenity", "Tranquility", "Calm", "Drift", "Horizon", "Breeze", "Stillness"],
        "melancholic": ["Twilight", "Reverie", "Remembrance", "Echoes", "Whispers", "Solitude", "Dusk"],
        "mysterious": ["Enigma", "Secrets", "Labyrinth", "Veil", "Illusion", "Riddle", "Mystique"],
        "romantic": ["Passion", "Embrace", "Desire", "Yearning", "Devotion", "Ardor", "Enchantment"],
        "epic": ["Odyssey", "Triumph", "Legend", "Saga", "Conquest", "Majesty", "Grandeur"],
        "dark": ["Abyss", "Shadows", "Darkness", "Void", "Descent", "Eclipse", "Midnight"],
        "ethereal": ["Celestial", "Ethereal", "Astral", "Dreamscape", "Transcendence", "Nebula", "Aurora"]
    }
    
    # Title patterns by genre
    genre_patterns = {
        "jazz": ["Blue {mood}", "{mood} in {key}", "{instrument} {mood}", "Midnight {mood}", "{mood} Suite"],
        "classical": ["{mood} Sonata", "{mood} Symphony", "{instrument} Concerto", "{mood} Rhapsody", "Prelude to {mood}"],
        "rock": ["{mood} Anthem", "Heart of {mood}", "{mood} Revolution", "Electric {mood}", "{instrument} {mood}"],
        "electronic": ["{mood} Waves", "Digital {mood}", "{mood} Sequence", "Synthetic {mood}", "{mood} Circuit"],
        "ambient": ["{mood} Atmosphere", "Endless {mood}", "{mood} Horizon", "Floating {mood}", "{mood} Landscape"],
        "pop": ["{mood} Dreams", "Perfect {mood}", "{mood} Tonight", "Forever {mood}", "{mood} Love"],
        "hip hop": ["{mood} Flow", "{mood} Beat", "Urban {mood}", "{mood} Rhythm", "{instrument} {mood}"],
        "folk": ["{mood} Ballad", "Tales of {mood}", "{mood} Journey", "Rustic {mood}", "{instrument} {mood}"],
        "metal": ["{mood} Fury", "Eternal {mood}", "{mood} Inferno", "Brutal {mood}", "{instrument} {mood}"],
        "blues": ["{mood} Blues", "Delta {mood}", "{mood} Road", "Midnight {mood}", "{instrument} {mood}"],
        "country": ["{mood} Trail", "Southern {mood}", "{mood} Heartland", "Country {mood}", "{instrument} {mood}"],
        "r&b": ["Soulful {mood}", "{mood} Groove", "Smooth {mood}", "Urban {mood}", "{instrument} {mood}"],
        "reggae": ["Island {mood}", "{mood} Vibration", "Reggae {mood}", "Tropical {mood}", "{instrument} {mood}"],
        "world": ["Global {mood}", "Ethnic {mood}", "Cultural {mood}", "Tribal {mood}", "{instrument} {mood}"],
        "soundtrack": ["{mood} Theme", "Cinematic {mood}", "{mood} Score", "Epic {mood}", "{instrument} {mood}"]
    }
    
    # Default to jazz if genre not found
    patterns = genre_patterns.get(genre.lower(), genre_patterns["jazz"])
    
    # Default to relaxed if mood not found
    mood_options = mood_words.get(mood.lower(), mood_words["relaxed"])
    
    # Random musical keys
    keys = ["A", "B", "C", "D", "E", "F", "G", "A minor", "B minor", "C minor", "D minor", "E minor", "F minor", "G minor"]
    
    # Select a random pattern and mood word
    pattern = random.choice(patterns)
    mood_word = random.choice(mood_options)
    key = random.choice(keys)
    
    # Select a random instrument if available
    instrument = random.choice(instruments) if instruments else "Piano"
    
    # Format the title
    title = pattern.format(mood=mood_word, key=key, instrument=instrument)
    
    return title 