import random
from typing import List, Dict, Any


def search_music_studios(args: dict) -> dict:
    """
    Search for music studios in a specified city with filters for equipment and price.
    Returns a list of studios with details including name, location, price, and equipment.
    """
    city = args.get("city", "").lower()
    equipment = args.get("equipment", "").lower()
    max_price = float(args.get("max_price_per_hour", 1000))
    
    # Generate mock data for music studios
    studios = generate_mock_studios(city, equipment, max_price)
    
    return {
        "city": city.capitalize(),
        "equipment_filter": equipment,
        "max_price_filter": max_price,
        "studios": studios
    }


def generate_mock_studios(city: str, equipment_filter: str, max_price: float) -> List[Dict[str, Any]]:
    """Generate mock music studio data based on search parameters."""
    # Define studio data by city
    studio_data = {
        "los angeles": [
            {
                "name": "Sunset Sound",
                "location": "Los Angeles",
                "price_per_hour": 150,
                "equipment": "Full drum recording setup, vintage mics, mixing console, Pro Tools HD",
                "room_size": "Large",
                "description": "Historic studio where countless hit records have been made since 1960."
            },
            {
                "name": "EastWest Studios",
                "location": "Los Angeles",
                "price_per_hour": 200,
                "equipment": "Isolated drum room, Pro Tools HD, Neve console, vintage synths",
                "room_size": "Large",
                "description": "World-class recording facility with multiple rooms and vintage equipment."
            },
            {
                "name": "The Village",
                "location": "Los Angeles",
                "price_per_hour": 175,
                "equipment": "SSL console, Pro Tools, grand piano, vintage outboard gear",
                "room_size": "Medium",
                "description": "Legendary studio with a rich history of recording iconic albums."
            },
            {
                "name": "Sound Factory",
                "location": "Los Angeles",
                "price_per_hour": 125,
                "equipment": "API console, drum kit, guitar amps, Pro Tools",
                "room_size": "Medium",
                "description": "Boutique studio with warm acoustics and vintage equipment."
            },
            {
                "name": "Kingsize Soundlabs",
                "location": "Los Angeles",
                "price_per_hour": 90,
                "equipment": "Analog recording, drum kit, guitar amps, basic outboard gear",
                "room_size": "Small",
                "description": "Affordable studio with a great collection of vintage instruments."
            }
        ],
        "new york": [
            {
                "name": "Electric Lady Studios",
                "location": "New York",
                "price_per_hour": 180,
                "equipment": "Vintage console, Pro Tools HD, extensive mic collection, isolation booths",
                "room_size": "Medium",
                "description": "Historic studio founded by Jimi Hendrix with a legendary sound."
            },
            {
                "name": "Avatar Studios",
                "location": "New York",
                "price_per_hour": 220,
                "equipment": "SSL console, Pro Tools, grand piano, extensive outboard gear",
                "room_size": "Large",
                "description": "World-class facility with multiple rooms and exceptional acoustics."
            },
            {
                "name": "Platinum Sound",
                "location": "New York",
                "price_per_hour": 160,
                "equipment": "SSL console, Pro Tools, drum kit, keyboard collection",
                "room_size": "Medium",
                "description": "Modern studio with state-of-the-art equipment and comfortable atmosphere."
            },
            {
                "name": "Dubway Studios",
                "location": "New York",
                "price_per_hour": 110,
                "equipment": "Pro Tools, Logic Pro, drum recording setup, vocal booth",
                "room_size": "Small",
                "description": "Versatile studio specializing in various recording needs."
            },
            {
                "name": "Flux Studios",
                "location": "New York",
                "price_per_hour": 95,
                "equipment": "Analog and digital recording, basic outboard gear, vocal booth",
                "room_size": "Small",
                "description": "Boutique studio with a creative atmosphere and quality gear."
            }
        ],
        "london": [
            {
                "name": "Abbey Road Studios",
                "location": "London",
                "price_per_hour": 250,
                "equipment": "Vintage consoles, extensive mic collection, grand piano, orchestral recording",
                "room_size": "Large",
                "description": "Iconic studio known for recording The Beatles and countless classic albums."
            },
            {
                "name": "RAK Studios",
                "location": "London",
                "price_per_hour": 180,
                "equipment": "Neve console, Pro Tools, vintage outboard gear, drum kit",
                "room_size": "Medium",
                "description": "Historic studio with excellent acoustics and vintage equipment."
            },
            {
                "name": "Metropolis Studios",
                "location": "London",
                "price_per_hour": 200,
                "equipment": "SSL console, Pro Tools HD, extensive mic collection, mastering suite",
                "room_size": "Large",
                "description": "Europe's largest independent recording facility with multiple studios."
            },
            {
                "name": "Strongroom Studios",
                "location": "London",
                "price_per_hour": 140,
                "equipment": "Neve console, Pro Tools, Logic Pro, drum recording setup",
                "room_size": "Medium",
                "description": "Versatile studio complex with multiple rooms and creative atmosphere."
            },
            {
                "name": "The Pool",
                "location": "London",
                "price_per_hour": 120,
                "equipment": "Analog recording, basic outboard gear, drum kit, guitar amps",
                "room_size": "Small",
                "description": "Unique studio built in a converted Victorian swimming pool."
            }
        ],
        "nashville": [
            {
                "name": "Blackbird Studio",
                "location": "Nashville",
                "price_per_hour": 170,
                "equipment": "Vintage consoles, extensive mic collection, grand piano, multiple isolation booths",
                "room_size": "Large",
                "description": "Premier Nashville studio with multiple rooms and exceptional gear."
            },
            {
                "name": "Sound Emporium",
                "location": "Nashville",
                "price_per_hour": 150,
                "equipment": "Neve console, Pro Tools HD, vintage outboard gear, string recording",
                "room_size": "Medium",
                "description": "Historic studio known for country and Americana recordings."
            },
            {
                "name": "RCA Studio B",
                "location": "Nashville",
                "price_per_hour": 190,
                "equipment": "Vintage equipment, piano, classic Nashville sound",
                "room_size": "Medium",
                "description": "Historic studio where Elvis Presley and many country legends recorded."
            },
            {
                "name": "Welcome to 1979",
                "location": "Nashville",
                "price_per_hour": 110,
                "equipment": "Analog tape machines, vintage gear, vinyl mastering",
                "room_size": "Medium",
                "description": "Analog-focused studio with vintage equipment and tape machines."
            },
            {
                "name": "The Tracking Room",
                "location": "Nashville",
                "price_per_hour": 160,
                "equipment": "SSL console, Pro Tools, extensive mic collection, grand piano",
                "room_size": "Large",
                "description": "Spacious studio with excellent acoustics for full band recordings."
            }
        ]
    }
    
    # Default to Los Angeles if city not found
    city_studios = studio_data.get(city.lower(), studio_data["los angeles"])
    
    # Filter by price
    filtered_studios = [studio for studio in city_studios if studio["price_per_hour"] <= max_price]
    
    # Filter by equipment if specified
    if equipment_filter:
        filtered_studios = [
            studio for studio in filtered_studios 
            if equipment_filter.lower() in studio["equipment"].lower()
        ]
    
    # Return at least some results even if filters are too restrictive
    if not filtered_studios and city_studios:
        # Return 2 random studios from the city if available
        return random.sample(city_studios, min(2, len(city_studios)))
    
    return filtered_studios 