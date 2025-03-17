import random
import string
from datetime import datetime


def book_studio_session(args: dict) -> dict:
    """
    Book a session at a music studio, specifying studio name, date, time, and duration.
    Returns booking details including booking ID, studio, date, times, and total cost.
    """
    studio_name = args.get("studio_name", "")
    date = args.get("date", "")
    start_time = args.get("start_time", "")
    duration_hours = float(args.get("duration_hours", 1.0))
    
    # Validate inputs
    if not all([studio_name, date, start_time]):
        return {"error": "Missing required booking information"}
    
    try:
        # Parse date and time
        booking_date = datetime.strptime(date, "%Y-%m-%d")
        start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        
        # Calculate end time
        hours = int(duration_hours)
        minutes = int((duration_hours - hours) * 60)
        end_hour = (start_datetime.hour + hours) % 24
        end_minute = (start_datetime.minute + minutes) % 60
        if start_datetime.minute + minutes >= 60:
            end_hour = (end_hour + 1) % 24
        
        end_time = f"{end_hour:02d}:{end_minute:02d}"
        
    except ValueError:
        return {"error": "Invalid date or time format"}
    
    # Generate a booking reference
    booking_id = generate_booking_reference(studio_name, date)
    
    # Calculate total cost (mock data)
    hourly_rates = {
        "Sunset Sound": 150,
        "EastWest Studios": 200,
        "The Village": 175,
        "Sound Factory": 125,
        "Kingsize Soundlabs": 90,
        "Electric Lady Studios": 180,
        "Avatar Studios": 220,
        "Platinum Sound": 160,
        "Dubway Studios": 110,
        "Flux Studios": 95,
        "Abbey Road Studios": 250,
        "RAK Studios": 180,
        "Metropolis Studios": 200,
        "Strongroom Studios": 140,
        "The Pool": 120,
        "Blackbird Studio": 170,
        "Sound Emporium": 150,
        "RCA Studio B": 190,
        "Welcome to 1979": 110,
        "The Tracking Room": 160
    }
    
    hourly_rate = hourly_rates.get(studio_name, 150)  # Default to $150/hour if studio not found
    total_cost = hourly_rate * duration_hours
    
    return {
        "booking_id": booking_id,
        "studio": studio_name,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "duration_hours": duration_hours,
        "hourly_rate": hourly_rate,
        "total_cost": total_cost,
        "status": "confirmed"
    }


def generate_booking_reference(studio_name: str, date: str) -> str:
    """Generate a unique booking reference."""
    # Extract studio initials
    initials = ''.join([word[0] for word in studio_name.split() if word])
    if not initials:
        initials = "SS"  # Default if no initials can be extracted
    
    # Extract date components
    try:
        booking_date = datetime.strptime(date, "%Y-%m-%d")
        date_part = f"{booking_date.year}-{booking_date.month:02d}{booking_date.day:02d}"
    except ValueError:
        date_part = datetime.now().strftime("%Y-%m%d")
    
    # Generate random suffix
    random_suffix = ''.join(random.choices(string.digits, k=1))
    
    return f"{initials}-{date_part}-{random_suffix}" 