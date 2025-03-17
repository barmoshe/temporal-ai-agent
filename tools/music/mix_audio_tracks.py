import json
import random
from typing import Dict, Any, List


def mix_audio_tracks(args: dict) -> dict:
    """
    Mixes multiple audio tracks with adjustable levels and effects.
    
    Args:
        args: Dictionary containing the following keys:
            - tracks: JSON string of track objects with URLs and volume levels
            - output_format: Optional output format (default: 'mp3')
            - apply_mastering: Optional whether to apply mastering (default: True)
            
    Returns:
        Dictionary containing the mixed audio information
    """
    tracks_str = args.get("tracks", "[]")
    output_format = args.get("output_format", "mp3")
    apply_mastering = args.get("apply_mastering", True)
    
    # Parse the tracks JSON
    try:
        tracks = json.loads(tracks_str)
        if not isinstance(tracks, list):
            tracks = []
    except json.JSONDecodeError:
        # If the JSON is invalid, create an empty list
        tracks = []
    
    # Validate and process the tracks
    processed_tracks = []
    for track in tracks:
        if isinstance(track, dict) and "url" in track:
            # Ensure volume is a number between 0 and 100
            volume = float(track.get("volume", 100))
            volume = max(0, min(100, volume))
            
            # Ensure pan is a number between -100 and 100
            pan = float(track.get("pan", 0))
            pan = max(-100, min(100, pan))
            
            # Add the processed track
            processed_tracks.append({
                "url": track["url"],
                "name": track.get("name", f"Track {len(processed_tracks) + 1}"),
                "volume": volume,
                "pan": pan,
                "mute": bool(track.get("mute", False)),
                "solo": bool(track.get("solo", False)),
                "effects": track.get("effects", [])
            })
    
    # If no valid tracks were provided, return an error
    if not processed_tracks:
        return {
            "success": False,
            "error": "No valid tracks provided"
        }
    
    # Generate a mix description
    mix_description = f"Mixed {len(processed_tracks)} tracks with mastering" if apply_mastering else f"Mixed {len(processed_tracks)} tracks without mastering"
    
    # Generate a mock mixed audio URL
    timestamp = random.randint(10000000, 99999999)
    mixed_audio_url = f"/compositions/mixes/mix_{timestamp}.{output_format}"
    
    # Generate a mock waveform image URL
    waveform_image = f"/compositions/waveforms/mix_{timestamp}.png"
    
    # Generate a mock mixing report
    mixing_report = generate_mixing_report(processed_tracks, apply_mastering)
    
    return {
        "success": True,
        "mix_description": mix_description,
        "tracks": processed_tracks,
        "output_format": output_format,
        "apply_mastering": apply_mastering,
        "mixed_audio_url": mixed_audio_url,
        "waveform_image": waveform_image,
        "mixing_report": mixing_report
    }


def generate_mixing_report(tracks: List[Dict[str, Any]], apply_mastering: bool) -> Dict[str, Any]:
    """
    Generate a report of the mixing process.
    
    Args:
        tracks: List of processed track objects
        apply_mastering: Whether mastering was applied
        
    Returns:
        Dictionary containing the mixing report
    """
    # Calculate the peak level (simulated)
    peak_level = -random.uniform(0.5, 6.0)
    
    # Calculate the RMS level (simulated)
    rms_level = peak_level - random.uniform(6.0, 12.0)
    
    # Calculate the dynamic range (simulated)
    dynamic_range = random.uniform(6.0, 14.0)
    
    # Calculate the stereo width (simulated)
    stereo_width = random.uniform(70.0, 95.0)
    
    # Generate frequency balance (simulated)
    frequency_balance = {
        "low": random.uniform(80.0, 100.0),
        "mid": random.uniform(85.0, 100.0),
        "high": random.uniform(75.0, 95.0)
    }
    
    # Generate applied effects
    applied_effects = []
    
    # Add track-specific effects
    for track in tracks:
        for effect in track.get("effects", []):
            effect_name = effect.get("name", "Unknown Effect")
            if effect_name not in [e["name"] for e in applied_effects]:
                applied_effects.append({
                    "name": effect_name,
                    "type": effect.get("type", "Unknown"),
                    "settings": effect.get("settings", {})
                })
    
    # Add mastering effects if applied
    if apply_mastering:
        mastering_effects = [
            {
                "name": "EQ",
                "type": "equalizer",
                "settings": {
                    "low_shelf": f"+{random.uniform(0.5, 2.0):.1f} dB @ 100 Hz",
                    "high_shelf": f"+{random.uniform(0.5, 1.5):.1f} dB @ 10 kHz",
                    "mid_cut": f"-{random.uniform(0.5, 1.0):.1f} dB @ 400 Hz"
                }
            },
            {
                "name": "Compressor",
                "type": "dynamics",
                "settings": {
                    "threshold": f"-{random.uniform(12.0, 18.0):.1f} dB",
                    "ratio": f"{random.uniform(1.5, 3.0):.1f}:1",
                    "attack": f"{random.uniform(5.0, 20.0):.1f} ms",
                    "release": f"{random.uniform(50.0, 200.0):.1f} ms"
                }
            },
            {
                "name": "Limiter",
                "type": "dynamics",
                "settings": {
                    "threshold": f"-{random.uniform(0.5, 2.0):.1f} dB",
                    "ceiling": "0.0 dB",
                    "release": f"{random.uniform(10.0, 50.0):.1f} ms"
                }
            }
        ]
        applied_effects.extend(mastering_effects)
    
    # Generate the report
    report = {
        "levels": {
            "peak": f"{peak_level:.1f} dB",
            "rms": f"{rms_level:.1f} dB",
            "dynamic_range": f"{dynamic_range:.1f} dB",
            "stereo_width": f"{stereo_width:.1f}%"
        },
        "frequency_balance": {
            "low": f"{frequency_balance['low']:.1f}%",
            "mid": f"{frequency_balance['mid']:.1f}%",
            "high": f"{frequency_balance['high']:.1f}%"
        },
        "applied_effects": applied_effects,
        "mastering_applied": apply_mastering,
        "clipping_detected": peak_level > -0.1,
        "phase_issues_detected": random.random() < 0.2,  # 20% chance of phase issues
        "recommendations": generate_recommendations(peak_level, rms_level, dynamic_range, frequency_balance)
    }
    
    return report


def generate_recommendations(peak_level: float, rms_level: float, dynamic_range: float, frequency_balance: Dict[str, float]) -> List[str]:
    """
    Generate mixing recommendations based on the analysis.
    
    Args:
        peak_level: Peak level in dB
        rms_level: RMS level in dB
        dynamic_range: Dynamic range in dB
        frequency_balance: Dictionary of frequency balance percentages
        
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Check peak level
    if peak_level > -0.5:
        recommendations.append("Reduce overall level to avoid clipping")
    elif peak_level < -6.0:
        recommendations.append("Increase overall level for better signal-to-noise ratio")
    
    # Check dynamic range
    if dynamic_range < 8.0:
        recommendations.append("Reduce compression to increase dynamic range")
    elif dynamic_range > 12.0:
        recommendations.append("Consider more compression for a more consistent sound")
    
    # Check frequency balance
    if frequency_balance["low"] > 95.0:
        recommendations.append("Reduce low frequencies to avoid muddiness")
    elif frequency_balance["low"] < 85.0:
        recommendations.append("Boost low frequencies for more warmth")
    
    if frequency_balance["mid"] > 95.0:
        recommendations.append("Reduce mid frequencies to avoid boxiness")
    elif frequency_balance["mid"] < 85.0:
        recommendations.append("Boost mid frequencies for more presence")
    
    if frequency_balance["high"] > 90.0:
        recommendations.append("Reduce high frequencies to avoid harshness")
    elif frequency_balance["high"] < 80.0:
        recommendations.append("Boost high frequencies for more clarity")
    
    # Add some general recommendations
    general_recommendations = [
        "Consider adding reverb for more spatial depth",
        "Try parallel compression on drums for more punch",
        "Experiment with stereo widening on background elements",
        "Consider automating volume for dynamic sections",
        "Try side-chain compression for better clarity between bass and kick"
    ]
    
    # Add 1-2 general recommendations
    num_general = random.randint(1, 2)
    selected_general = random.sample(general_recommendations, min(num_general, len(general_recommendations)))
    recommendations.extend(selected_general)
    
    return recommendations 