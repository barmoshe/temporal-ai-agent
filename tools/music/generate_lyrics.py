import random
from typing import Dict, Any, List


def generate_lyrics(args: dict) -> dict:
    """
    Generates song lyrics based on specified theme, mood, and structure.
    
    Args:
        args: Dictionary containing the following keys:
            - theme: Main theme or topic of the lyrics
            - mood: Emotional mood (e.g., 'happy', 'sad', 'reflective')
            - structure: Optional song structure (default: 'verse-chorus-verse-chorus')
            - style: Optional lyrical style (default: 'narrative')
            
    Returns:
        Dictionary containing the generated lyrics information
    """
    theme = args.get("theme", "love")
    mood = args.get("mood", "reflective")
    structure = args.get("structure", "verse-chorus-verse-chorus")
    style = args.get("style", "narrative")
    
    # Generate a title based on the theme and mood
    title = generate_song_title(theme, mood)
    
    # Parse the structure
    sections = structure.split("-")
    
    # Generate lyrics for each section
    lyrics = {}
    full_text = []
    
    for i, section in enumerate(sections):
        section_key = f"{section}{i+1 if sections.count(section) > 1 and section != 'bridge' and section != 'chorus' else ''}"
        
        # Generate lyrics for this section
        section_lyrics = generate_section_lyrics(section, theme, mood, style)
        lyrics[section_key] = section_lyrics
        
        # Add to the full text
        full_text.append(f"[{section.upper()}]")
        full_text.append(section_lyrics)
        full_text.append("")  # Empty line between sections
    
    # Create a theme analysis
    theme_analysis = f"These lyrics explore the theme of {theme} through a {mood} emotional lens, using {style} storytelling techniques."
    
    return {
        "success": True,
        "title": title,
        "lyrics": lyrics,
        "full_text": "\n".join(full_text),
        "theme": theme,
        "mood": mood,
        "structure": structure,
        "style": style,
        "theme_analysis": theme_analysis
    }


def generate_song_title(theme: str, mood: str) -> str:
    """
    Generate a creative song title based on the theme and mood.
    
    Args:
        theme: The main theme or topic
        mood: The emotional mood
        
    Returns:
        A song title
    """
    # Title patterns
    patterns = [
        "The {theme} of {mood}",
        "{mood} {theme}",
        "{theme} in the {time}",
        "When the {theme} {action}",
        "{adjective} {theme}",
        "{theme} and {related}",
        "The Last {theme}",
        "{number} {theme}s",
        "{theme} of the {place}",
        "{color} {theme}",
    ]
    
    # Theme-related words
    theme_words = {
        "love": ["heart", "embrace", "passion", "desire", "romance", "affection"],
        "loss": ["goodbye", "farewell", "emptiness", "void", "absence", "memory"],
        "hope": ["dream", "future", "horizon", "light", "promise", "tomorrow"],
        "freedom": ["liberation", "escape", "journey", "wings", "chains", "flight"],
        "time": ["moment", "hour", "eternity", "clock", "memory", "yesterday"],
        "nature": ["river", "mountain", "ocean", "forest", "sky", "wilderness"],
        "city": ["streets", "lights", "skyline", "concrete", "crowd", "building"],
        "dreams": ["sleep", "vision", "fantasy", "imagination", "subconscious", "reality"],
        "change": ["transformation", "evolution", "metamorphosis", "shift", "transition", "rebirth"],
        "struggle": ["battle", "fight", "challenge", "obstacle", "adversity", "triumph"],
    }
    
    # Mood-related adjectives
    mood_adjectives = {
        "happy": ["joyful", "ecstatic", "blissful", "radiant", "euphoric", "delighted"],
        "sad": ["melancholic", "sorrowful", "mournful", "wistful", "heartbroken", "forlorn"],
        "angry": ["furious", "raging", "seething", "fierce", "burning", "intense"],
        "peaceful": ["serene", "tranquil", "calm", "gentle", "harmonious", "still"],
        "reflective": ["thoughtful", "contemplative", "introspective", "pensive", "meditative", "philosophical"],
        "anxious": ["nervous", "restless", "uneasy", "tense", "worried", "apprehensive"],
        "nostalgic": ["reminiscent", "yearning", "longing", "sentimental", "wistful", "retrospective"],
        "hopeful": ["optimistic", "promising", "expectant", "aspiring", "encouraging", "uplifting"],
        "mysterious": ["enigmatic", "cryptic", "veiled", "shadowy", "obscure", "elusive"],
        "passionate": ["ardent", "fervent", "intense", "fiery", "zealous", "vehement"],
    }
    
    # Time-related words
    times = ["night", "morning", "dusk", "dawn", "twilight", "midnight", "sunset", "hour"]
    
    # Action verbs
    actions = ["falls", "rises", "breaks", "heals", "fades", "shines", "burns", "whispers", "calls", "dances"]
    
    # Related concepts
    related_concepts = {
        "love": ["loss", "time", "memory", "distance", "truth", "lies"],
        "loss": ["love", "memory", "time", "healing", "pain", "acceptance"],
        "hope": ["despair", "faith", "future", "dream", "reality", "possibility"],
        "freedom": ["captivity", "control", "choice", "destiny", "fate", "will"],
        "time": ["space", "memory", "moment", "eternity", "change", "constancy"],
        "nature": ["humanity", "technology", "wilderness", "civilization", "harmony", "chaos"],
        "city": ["solitude", "crowd", "noise", "silence", "rhythm", "pace"],
        "dreams": ["reality", "awakening", "sleep", "consciousness", "illusion", "truth"],
        "change": ["constancy", "tradition", "innovation", "resistance", "acceptance", "adaptation"],
        "struggle": ["peace", "victory", "defeat", "resilience", "surrender", "perseverance"],
    }
    
    # Places
    places = ["heart", "mind", "city", "wilderness", "ocean", "mountain", "desert", "night", "storm", "silence"]
    
    # Colors
    colors = ["blue", "red", "golden", "silver", "crimson", "azure", "emerald", "violet", "amber", "obsidian"]
    
    # Numbers
    numbers = ["thousand", "million", "hundred", "seven", "three", "infinite", "countless", "single", "last", "first"]
    
    # Get theme-related words or use defaults
    theme_related = theme_words.get(theme.lower(), [theme, "moment", "feeling", "thought", "dream", "memory"])
    theme_word = random.choice([theme] + theme_related)
    
    # Get mood-related adjectives or use defaults
    mood_related = mood_adjectives.get(mood.lower(), [mood, "deep", "intense", "subtle", "profound", "vivid"])
    mood_word = random.choice([mood] + mood_related)
    
    # Get related concepts or use defaults
    related_options = related_concepts.get(theme.lower(), ["memory", "moment", "feeling", "thought", "dream", "reality"])
    related_word = random.choice(related_options)
    
    # Choose a pattern and fill it
    pattern = random.choice(patterns)
    
    title = pattern.format(
        theme=theme_word.title(),
        mood=mood_word.title(),
        time=random.choice(times).title(),
        action=random.choice(actions),
        adjective=random.choice(mood_related).title(),
        related=related_word.title(),
        place=random.choice(places).title(),
        color=random.choice(colors).title(),
        number=random.choice(numbers).title()
    )
    
    return title


def generate_section_lyrics(section: str, theme: str, mood: str, style: str) -> str:
    """
    Generate lyrics for a specific section of the song.
    
    Args:
        section: The section type (verse, chorus, bridge, etc.)
        theme: The main theme or topic
        mood: The emotional mood
        style: The lyrical style
        
    Returns:
        Lyrics for the section
    """
    # Define section characteristics
    section_patterns = {
        "verse": {
            "lines": 8,
            "rhyme_scheme": "ABABCDCD",
            "focus": "narrative",
            "line_length": "medium",
        },
        "chorus": {
            "lines": 4,
            "rhyme_scheme": "AABB",
            "focus": "hook",
            "line_length": "short",
        },
        "bridge": {
            "lines": 4,
            "rhyme_scheme": "CDCD",
            "focus": "contrast",
            "line_length": "medium",
        },
        "pre-chorus": {
            "lines": 2,
            "rhyme_scheme": "AA",
            "focus": "buildup",
            "line_length": "medium",
        },
        "outro": {
            "lines": 2,
            "rhyme_scheme": "AA",
            "focus": "conclusion",
            "line_length": "medium",
        },
        "intro": {
            "lines": 2,
            "rhyme_scheme": "AA",
            "focus": "setup",
            "line_length": "short",
        },
    }
    
    # Default to verse if section not found
    section_info = section_patterns.get(section.lower(), section_patterns["verse"])
    
    # Theme-related vocabulary
    theme_vocabulary = {
        "love": [
            "heart", "soul", "embrace", "touch", "kiss", "eyes", "hands", "arms",
            "forever", "always", "never", "together", "apart", "close", "far",
            "feel", "hold", "miss", "need", "want", "desire", "yearn", "long",
            "passion", "flame", "fire", "burn", "glow", "light", "dark",
        ],
        "loss": [
            "goodbye", "farewell", "end", "gone", "empty", "hollow", "void", "absence",
            "memory", "forget", "remember", "past", "never", "always", "forever",
            "tears", "pain", "hurt", "wound", "scar", "heal", "break", "shatter",
            "shadow", "ghost", "echo", "whisper", "silence", "still", "quiet",
        ],
        "hope": [
            "dream", "wish", "pray", "believe", "faith", "trust", "future", "tomorrow",
            "light", "shine", "glow", "bright", "dark", "shadow", "dawn", "sunrise",
            "rise", "climb", "reach", "grasp", "hold", "cling", "release", "let go",
            "horizon", "sky", "star", "moon", "sun", "cloud", "rain", "rainbow",
        ],
        "freedom": [
            "fly", "soar", "wings", "sky", "horizon", "open", "wide", "vast",
            "chains", "break", "escape", "flee", "run", "leave", "stay", "return",
            "choice", "path", "road", "journey", "destination", "map", "compass", "guide",
            "wind", "breath", "air", "space", "room", "wall", "door", "window",
        ],
    }
    
    # Mood-related vocabulary
    mood_vocabulary = {
        "happy": [
            "smile", "laugh", "joy", "delight", "pleasure", "bliss", "ecstasy", "euphoria",
            "bright", "shine", "glow", "radiate", "beam", "sparkle", "glitter", "gleam",
            "dance", "sing", "celebrate", "rejoice", "embrace", "kiss", "touch", "hold",
            "sun", "light", "day", "morning", "spring", "summer", "warm", "golden",
        ],
        "sad": [
            "cry", "tears", "sob", "weep", "mourn", "grieve", "lament", "sorrow",
            "dark", "dim", "fade", "shadow", "gray", "black", "blue", "cold",
            "fall", "sink", "drown", "suffocate", "choke", "gasp", "breathe", "sigh",
            "rain", "storm", "cloud", "fog", "mist", "night", "winter", "autumn",
        ],
        "reflective": [
            "think", "ponder", "wonder", "question", "answer", "search", "find", "lose",
            "deep", "shallow", "surface", "beneath", "above", "below", "inside", "outside",
            "remember", "forget", "recall", "reminisce", "revisit", "return", "remain", "leave",
            "mirror", "reflection", "image", "shadow", "echo", "ripple", "wave", "still",
        ],
    }
    
    # Style-related patterns
    style_patterns = {
        "narrative": {
            "first_person": True,
            "tense": "past",
            "descriptive": True,
            "metaphorical": False,
        },
        "abstract": {
            "first_person": False,
            "tense": "present",
            "descriptive": False,
            "metaphorical": True,
        },
        "rhyming": {
            "first_person": True,
            "tense": "present",
            "descriptive": True,
            "metaphorical": True,
        },
        "conversational": {
            "first_person": True,
            "tense": "present",
            "descriptive": False,
            "metaphorical": False,
        },
    }
    
    # Default to narrative if style not found
    style_info = style_patterns.get(style.lower(), style_patterns["narrative"])
    
    # Get vocabulary for the theme and mood
    theme_words = theme_vocabulary.get(theme.lower(), theme_vocabulary.get("love", []))
    mood_words = mood_vocabulary.get(mood.lower(), mood_vocabulary.get("reflective", []))
    
    # Combined vocabulary
    vocabulary = theme_words + mood_words
    
    # Generate lines based on section characteristics
    lines = []
    
    # Different approaches based on section type
    if section.lower() == "chorus":
        # Choruses are more repetitive and hook-focused
        hook_line = generate_hook_line(theme, mood, vocabulary)
        lines.append(hook_line)
        
        # Add supporting lines
        for i in range(1, section_info["lines"]):
            if i == section_info["lines"] - 1:
                # Repeat the hook at the end
                lines.append(hook_line)
            else:
                lines.append(generate_line(theme, mood, vocabulary, style_info, section_info["line_length"]))
    
    elif section.lower() == "bridge":
        # Bridges often provide contrast or new perspective
        for i in range(section_info["lines"]):
            # Use more metaphorical language in bridges
            bridge_style = style_info.copy()
            bridge_style["metaphorical"] = True
            lines.append(generate_line(theme, mood, vocabulary, bridge_style, section_info["line_length"]))
    
    else:  # verse, pre-chorus, outro, intro
        # Generate lines based on the section's characteristics
        for i in range(section_info["lines"]):
            lines.append(generate_line(theme, mood, vocabulary, style_info, section_info["line_length"]))
    
    # Join the lines into a single string
    return "\n".join(lines)


def generate_hook_line(theme: str, mood: str, vocabulary: List[str]) -> str:
    """
    Generate a catchy hook line for a chorus.
    
    Args:
        theme: The main theme or topic
        mood: The emotional mood
        vocabulary: List of theme and mood related words
        
    Returns:
        A hook line
    """
    # Hook patterns
    patterns = [
        "I {verb} the {noun} of {theme}",
        "{theme} is all I {verb}",
        "We'll {verb} in the {noun} of {mood}",
        "This {theme} {verb}s like a {noun}",
        "Oh, {theme} {verb}s me {adverb}",
        "Don't {verb} my {theme} {adverb}",
        "{verb} me in the {noun} of {theme}",
        "I'll {verb} your {theme} {adverb}",
    ]
    
    # Verbs related to the theme and mood
    verbs = ["feel", "touch", "hold", "see", "hear", "taste", "smell", "sense", 
             "know", "remember", "forget", "miss", "need", "want", "love", "hate"]
    
    # Nouns from vocabulary
    nouns = [word for word in vocabulary if len(word) > 3]
    
    # Adverbs
    adverbs = ["slowly", "quickly", "deeply", "lightly", "softly", "hardly", 
               "barely", "nearly", "almost", "forever", "never", "always", "again"]
    
    # Choose a pattern and fill it
    pattern = random.choice(patterns)
    
    hook = pattern.format(
        theme=theme,
        mood=mood,
        verb=random.choice(verbs),
        noun=random.choice(nouns) if nouns else "heart",
        adverb=random.choice(adverbs)
    )
    
    return hook


def generate_line(theme: str, mood: str, vocabulary: List[str], style_info: Dict[str, Any], line_length: str) -> str:
    """
    Generate a single line of lyrics.
    
    Args:
        theme: The main theme or topic
        mood: The emotional mood
        vocabulary: List of theme and mood related words
        style_info: Dictionary of style characteristics
        line_length: Desired line length (short, medium, long)
        
    Returns:
        A line of lyrics
    """
    # Line patterns based on style
    first_person = style_info["first_person"]
    tense = style_info["tense"]
    descriptive = style_info["descriptive"]
    metaphorical = style_info["metaphorical"]
    
    # Subject pronouns
    subject = "I" if first_person else random.choice(["You", "We", "They", "She", "He", theme.title()])
    
    # Verb tense adjustments
    present_verbs = ["feel", "see", "hear", "touch", "taste", "know", "want", "need", "love", "hate", "miss", "remember", "forget"]
    past_verbs = ["felt", "saw", "heard", "touched", "tasted", "knew", "wanted", "needed", "loved", "hated", "missed", "remembered", "forgot"]
    
    verbs = past_verbs if tense == "past" else present_verbs
    
    # Line structure based on length
    if line_length == "short":
        # Short lines (3-5 words)
        patterns = [
            "{subject} {verb} the {noun}",
            "{subject} {verb} {adverb}",
            "The {noun} {verb}s {adverb}",
            "{adverb} {subject} {verb}",
        ]
    elif line_length == "long":
        # Long lines (8-12 words)
        patterns = [
            "{subject} {verb} the {noun} that {verb}s in the {noun} of {theme}",
            "When the {noun} {verb}s, {subject} {verb} the {noun} of {mood}",
            "{subject} {verb} {adverb} through the {noun} like a {noun} in {mood}",
            "The {noun} of {theme} {verb}s {adverb} as {subject} {verb} the {noun}",
        ]
    else:  # medium
        # Medium lines (6-8 words)
        patterns = [
            "{subject} {verb} the {noun} of {theme}",
            "In the {noun} of {mood}, {subject} {verb}",
            "{subject} {verb} {adverb} through the {noun}",
            "Like a {noun} in {mood}, {subject} {verb}",
        ]
    
    # Add metaphorical patterns if needed
    if metaphorical:
        metaphor_patterns = [
            "{theme} is a {noun} that {verb}s {adverb}",
            "Your {noun} is like a {theme} in {mood}",
            "The {noun} of {theme} {verb}s like {mood}",
            "{mood} {verb}s through me like a {noun}",
        ]
        patterns.extend(metaphor_patterns)
    
    # Add descriptive patterns if needed
    if descriptive:
        descriptive_patterns = [
            "The {adjective} {noun} {verb}s in the {noun}",
            "{subject} {verb} the {adjective} {noun} of {theme}",
            "{adjective} and {adjective}, the {noun} {verb}s",
            "Through the {adjective} {noun}, {subject} {verb}",
        ]
        patterns.extend(descriptive_patterns)
    
    # Choose random words from vocabulary
    nouns = [word for word in vocabulary if len(word) > 3]
    adjectives = [word for word in vocabulary if len(word) > 3]
    adverbs = ["slowly", "quickly", "deeply", "lightly", "softly", "hardly", 
               "barely", "nearly", "almost", "forever", "never", "always", "again"]
    
    # Choose a pattern and fill it
    pattern = random.choice(patterns)
    
    # Replace placeholders with words
    line = pattern.format(
        subject=subject,
        verb=random.choice(verbs),
        noun=random.choice(nouns) if nouns else "heart",
        theme=theme,
        mood=mood,
        adjective=random.choice(adjectives) if adjectives else "deep",
        adverb=random.choice(adverbs)
    )
    
    # Capitalize the first letter
    return line[0].upper() + line[1:] 