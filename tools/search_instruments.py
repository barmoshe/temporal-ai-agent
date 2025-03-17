import random
from typing import List, Dict, Any


def search_instruments(args: dict) -> dict:
    """
    Search for musical instruments by type, brand, and price range.
    Returns a list of instruments with details including name, type, and price.
    """
    instrument_type = args.get("instrument_type", "").lower()
    brand = args.get("brand", "").lower()
    max_price = float(args.get("max_price", 100000))
    
    # Generate mock data for instruments
    instruments = generate_mock_instruments(instrument_type, brand, max_price)
    
    return {
        "instrument_type": instrument_type.capitalize() if instrument_type else "All types",
        "brand_filter": brand.capitalize() if brand else "All brands",
        "max_price_filter": max_price,
        "instruments": instruments
    }


def generate_mock_instruments(instrument_type: str, brand: str, max_price: float) -> List[Dict[str, Any]]:
    """Generate mock instrument data based on search parameters."""
    # Define instrument data by type
    instrument_data = {
        "piano": [
            {
                "name": "Yamaha U3 Upright Piano",
                "type": "Piano",
                "brand": "Yamaha",
                "price": 8500,
                "description": "Professional upright piano with rich tone and responsive action."
            },
            {
                "name": "Steinway Model B Grand Piano",
                "type": "Piano",
                "brand": "Steinway",
                "price": 95000,
                "description": "Classic 6'11\" grand piano with exceptional sound quality and craftsmanship."
            },
            {
                "name": "Kawai K-500 Upright Piano",
                "type": "Piano",
                "brand": "Kawai",
                "price": 7200,
                "description": "Professional upright piano with excellent tone and touch."
            },
            {
                "name": "Roland FP-90X Digital Piano",
                "type": "Piano",
                "brand": "Roland",
                "price": 1800,
                "description": "High-end digital piano with authentic feel and sound."
            },
            {
                "name": "Bösendorfer 200 Grand Piano",
                "type": "Piano",
                "brand": "Bösendorfer",
                "price": 150000,
                "description": "Handcrafted grand piano with distinctive Viennese sound."
            }
        ],
        "guitar": [
            {
                "name": "Fender American Professional II Stratocaster",
                "type": "Guitar",
                "brand": "Fender",
                "price": 1700,
                "description": "Professional electric guitar with versatile tone and playability."
            },
            {
                "name": "Gibson Les Paul Standard '60s",
                "type": "Guitar",
                "brand": "Gibson",
                "price": 2500,
                "description": "Iconic electric guitar with rich, warm tone and sustain."
            },
            {
                "name": "Martin D-28 Acoustic Guitar",
                "type": "Guitar",
                "brand": "Martin",
                "price": 3200,
                "description": "Legendary dreadnought acoustic with rich bass and projection."
            },
            {
                "name": "Taylor 814ce Acoustic-Electric Guitar",
                "type": "Guitar",
                "brand": "Taylor",
                "price": 3700,
                "description": "Premium acoustic-electric with exceptional tone and electronics."
            },
            {
                "name": "PRS Custom 24 Electric Guitar",
                "type": "Guitar",
                "brand": "PRS",
                "price": 4000,
                "description": "Versatile electric guitar with premium tonewoods and craftsmanship."
            }
        ],
        "saxophone": [
            {
                "name": "Selmer Paris Series III Saxophone",
                "type": "Saxophone",
                "brand": "Selmer",
                "price": 7200,
                "description": "Professional alto saxophone with exceptional response and projection."
            },
            {
                "name": "Yamaha YAS-875EX Alto Saxophone",
                "type": "Saxophone",
                "brand": "Yamaha",
                "price": 4500,
                "description": "Professional alto saxophone with rich tone and excellent intonation."
            },
            {
                "name": "Yanagisawa A-WO2 Alto Saxophone",
                "type": "Saxophone",
                "brand": "Yanagisawa",
                "price": 5800,
                "description": "Professional bronze alto saxophone with warm, rich tone."
            },
            {
                "name": "Keilwerth SX90R Shadow Tenor Saxophone",
                "type": "Saxophone",
                "brand": "Keilwerth",
                "price": 6300,
                "description": "Professional tenor saxophone with powerful projection and unique finish."
            },
            {
                "name": "P. Mauriat PMXT-66R Tenor Saxophone",
                "type": "Saxophone",
                "brand": "P. Mauriat",
                "price": 3900,
                "description": "Professional tenor saxophone with vintage sound and modern reliability."
            }
        ],
        "drums": [
            {
                "name": "DW Collector's Series 5-Piece Shell Pack",
                "type": "Drums",
                "brand": "DW",
                "price": 4500,
                "description": "Premium maple drum kit with exceptional tone and craftsmanship."
            },
            {
                "name": "Tama Starclassic Walnut/Birch 4-Piece Shell Pack",
                "type": "Drums",
                "brand": "Tama",
                "price": 2800,
                "description": "Professional drum kit with warm tone and excellent projection."
            },
            {
                "name": "Pearl Masters Maple Complete 4-Piece Shell Pack",
                "type": "Drums",
                "brand": "Pearl",
                "price": 2300,
                "description": "Professional maple drum kit with versatile sound and reliability."
            },
            {
                "name": "Gretsch USA Custom 4-Piece Shell Pack",
                "type": "Drums",
                "brand": "Gretsch",
                "price": 4200,
                "description": "Handcrafted drum kit with classic tone and modern features."
            },
            {
                "name": "Sonor SQ2 4-Piece Shell Pack",
                "type": "Drums",
                "brand": "Sonor",
                "price": 5500,
                "description": "Premium customizable drum kit with exceptional build quality."
            }
        ],
        "synthesizer": [
            {
                "name": "Moog One 16-Voice Analog Synthesizer",
                "type": "Synthesizer",
                "brand": "Moog",
                "price": 8500,
                "description": "Flagship polyphonic analog synthesizer with incredible sound design capabilities."
            },
            {
                "name": "Sequential Prophet-5 Rev4",
                "type": "Synthesizer",
                "brand": "Sequential",
                "price": 3500,
                "description": "Legendary analog synthesizer with vintage sound and modern reliability."
            },
            {
                "name": "Korg Prologue 16-Voice Analog Synthesizer",
                "type": "Synthesizer",
                "brand": "Korg",
                "price": 2000,
                "description": "Professional analog synthesizer with digital multi-engine and effects."
            },
            {
                "name": "Roland Jupiter-X Synthesizer",
                "type": "Synthesizer",
                "brand": "Roland",
                "price": 2500,
                "description": "Flagship synthesizer with classic Roland sounds and modern features."
            },
            {
                "name": "Arturia MatrixBrute Analog Synthesizer",
                "type": "Synthesizer",
                "brand": "Arturia",
                "price": 2200,
                "description": "Powerful monophonic analog synthesizer with extensive modulation capabilities."
            }
        ],
        "violin": [
            {
                "name": "Stradivarius Model Violin",
                "type": "Violin",
                "brand": "Workshop",
                "price": 12000,
                "description": "Professional violin modeled after the famous Stradivarius design."
            },
            {
                "name": "Yamaha YVN Model 3 Violin",
                "type": "Violin",
                "brand": "Yamaha",
                "price": 2800,
                "description": "Professional violin with excellent projection and warm tone."
            },
            {
                "name": "Holstein Stradivari Copy Violin",
                "type": "Violin",
                "brand": "Holstein",
                "price": 5500,
                "description": "Handcrafted professional violin with exceptional tone and response."
            },
            {
                "name": "Scott Cao STV-850 Violin",
                "type": "Violin",
                "brand": "Scott Cao",
                "price": 3200,
                "description": "Professional violin with rich tone and excellent craftsmanship."
            },
            {
                "name": "Klaus Clement V33 Violin",
                "type": "Violin",
                "brand": "Klaus Clement",
                "price": 7500,
                "description": "Premium handcrafted violin with exceptional tonal qualities."
            }
        ]
    }
    
    # Collect all instruments if no specific type is requested
    if not instrument_type:
        all_instruments = []
        for instruments in instrument_data.values():
            all_instruments.extend(instruments)
        instruments_to_filter = all_instruments
    else:
        # Get instruments of the requested type, or default to piano if type not found
        instruments_to_filter = instrument_data.get(instrument_type.lower(), instrument_data["piano"])
    
    # Filter by price
    filtered_instruments = [
        instrument for instrument in instruments_to_filter 
        if instrument["price"] <= max_price
    ]
    
    # Filter by brand if specified
    if brand:
        filtered_instruments = [
            instrument for instrument in filtered_instruments 
            if brand.lower() in instrument["brand"].lower()
        ]
    
    # Return at least some results even if filters are too restrictive
    if not filtered_instruments and instruments_to_filter:
        # Return 2 random instruments from the original list if available
        return random.sample(instruments_to_filter, min(2, len(instruments_to_filter)))
    
    return filtered_instruments 