from datetime import datetime
from pathlib import Path
import json
import random


def find_music_events(args: dict) -> dict:
    """
    Find music events in a specified city and month, optionally filtered by genre.
    Returns a list of events with details including venue, date, genre, and ticket price.
    """
    search_city = args.get("city", "").lower()
    search_month = args.get("month", "").capitalize()
    search_genre = args.get("genre", "").capitalize()

    # Convert month name to month number
    try:
        month_number = datetime.strptime(search_month, "%B").month
    except ValueError:
        return {"error": "Invalid month provided."}

    # Generate mock data for music events
    events = generate_mock_music_events(search_city, month_number, search_genre)

    return {
        "city": search_city.capitalize(),
        "month": search_month,
        "genre": search_genre if search_genre else "All genres",
        "events": events
    }


def generate_mock_music_events(city: str, month: int, genre: str = None) -> list:
    """Generate mock music events data based on search parameters."""
    # Define some popular venues by city
    venues = {
        "new york": ["Madison Square Garden", "Radio City Music Hall", "Lincoln Center", "Blue Note Jazz Club", "Brooklyn Steel"],
        "los angeles": ["Hollywood Bowl", "The Greek Theatre", "Walt Disney Concert Hall", "The Troubadour", "The Roxy"],
        "london": ["Royal Albert Hall", "O2 Arena", "Wembley Stadium", "Ronnie Scott's Jazz Club", "Barbican Centre"],
        "paris": ["Olympia Hall", "Zenith Paris", "Philharmonie de Paris", "Le Bataclan", "AccorHotels Arena"],
        "tokyo": ["Budokan", "Tokyo Dome", "Blue Note Tokyo", "Billboard Live", "Suntory Hall"],
        "berlin": ["Waldbühne", "Mercedes-Benz Arena", "Philharmonie Berlin", "Berghain", "Tempodrom"],
        "sydney": ["Sydney Opera House", "Qudos Bank Arena", "Enmore Theatre", "State Theatre", "Metro Theatre"],
    }
    
    # Default to New York if city not found
    city_venues = venues.get(city.lower(), venues["new york"])
    
    # Define genres and associated artists
    genres_artists = {
        "rock": ["The Rolling Stones", "Foo Fighters", "Arctic Monkeys", "Radiohead", "Queens of the Stone Age"],
        "pop": ["Taylor Swift", "Dua Lipa", "The Weeknd", "Billie Eilish", "Harry Styles"],
        "jazz": ["Wynton Marsalis Quartet", "Kamasi Washington", "Norah Jones", "Gregory Porter", "Esperanza Spalding"],
        "classical": ["Berlin Philharmonic", "London Symphony Orchestra", "Yo-Yo Ma", "Lang Lang", "Vienna Philharmonic"],
        "electronic": ["Daft Punk", "Disclosure", "Four Tet", "Bonobo", "Aphex Twin"],
        "hip hop": ["Kendrick Lamar", "Tyler, The Creator", "J. Cole", "Anderson .Paak", "Run The Jewels"],
        "indie": ["Arcade Fire", "Tame Impala", "The National", "Vampire Weekend", "Fleet Foxes"],
    }
    
    # Filter by genre if provided
    if genre and genre.lower() in genres_artists:
        filtered_genres = {genre.lower(): genres_artists[genre.lower()]}
    else:
        filtered_genres = genres_artists
    
    # Generate random events
    events = []
    year = 2025
    
    for _ in range(random.randint(2, 5)):
        # Pick a random genre from filtered genres
        event_genre = random.choice(list(filtered_genres.keys()))
        # Pick a random artist from that genre
        artist = random.choice(filtered_genres[event_genre])
        # Pick a random venue
        venue = random.choice(city_venues)
        # Generate a random date in the specified month
        day = random.randint(1, 28)
        date = f"{year}-{month:02d}-{day:02d}"
        # Generate a random ticket price between $50 and $300
        ticket_price = round(random.uniform(50, 300), 2)
        
        events.append({
            "name": f"{artist} Concert",
            "artist": artist,
            "venue": venue,
            "date": date,
            "genre": event_genre.capitalize(),
            "ticket_price": ticket_price
        })
    
    return events 