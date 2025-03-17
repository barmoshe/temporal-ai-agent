import random
from typing import Dict, Any, List


def visualize_music(args: dict) -> dict:
    """
    Generates visual representations of music such as waveforms, spectrograms, or animated visualizations.
    
    Args:
        args: Dictionary containing the following keys:
            - audio_url: URL to the audio file to visualize
            - visualization_type: Type of visualization (e.g., 'waveform', 'spectrogram', 'animated')
            - color_scheme: Optional color scheme for the visualization (default: 'purple')
            
    Returns:
        Dictionary containing the visualization information
    """
    audio_url = args.get("audio_url", "")
    visualization_type = args.get("visualization_type", "waveform")
    color_scheme = args.get("color_scheme", "purple")
    
    # Validate inputs
    if not audio_url:
        return {
            "success": False,
            "error": "No audio URL provided"
        }
    
    # Generate visualization based on the type
    visualization_data = generate_visualization(audio_url, visualization_type, color_scheme)
    
    # Create a visualization description
    visualization_description = f"Generated a {color_scheme} {visualization_type} visualization for the audio"
    
    return {
        "success": True,
        "visualization_description": visualization_description,
        "audio_url": audio_url,
        "visualization_type": visualization_type,
        "color_scheme": color_scheme,
        "visualization_url": visualization_data["url"],
        "animated_url": visualization_data.get("animated_url", ""),
        "thumbnail_url": visualization_data.get("thumbnail_url", ""),
        "visualization_data": visualization_data.get("data", {})
    }


def generate_visualization(audio_url: str, visualization_type: str, color_scheme: str) -> Dict[str, Any]:
    """
    Generate visualization data based on the specified type and color scheme.
    
    Args:
        audio_url: URL to the audio file
        visualization_type: Type of visualization
        color_scheme: Color scheme for the visualization
        
    Returns:
        Dictionary containing visualization data
    """
    # Extract a unique identifier from the audio URL
    audio_id = audio_url.split("/")[-1].split(".")[0]
    
    # Define color schemes
    color_schemes = {
        "purple": {
            "primary": "#8A2BE2",
            "secondary": "#9370DB",
            "background": "#1E1E2E",
            "highlight": "#DA70D6",
            "text": "#FFFFFF"
        },
        "blue": {
            "primary": "#1E90FF",
            "secondary": "#00BFFF",
            "background": "#0A192F",
            "highlight": "#00FFFF",
            "text": "#FFFFFF"
        },
        "red": {
            "primary": "#FF4500",
            "secondary": "#FF6347",
            "background": "#2E1E1E",
            "highlight": "#FF0000",
            "text": "#FFFFFF"
        },
        "green": {
            "primary": "#00FA9A",
            "secondary": "#32CD32",
            "background": "#1E2E1E",
            "highlight": "#00FF00",
            "text": "#FFFFFF"
        },
        "gold": {
            "primary": "#FFD700",
            "secondary": "#FFA500",
            "background": "#2E2E1E",
            "highlight": "#FFFF00",
            "text": "#FFFFFF"
        },
        "monochrome": {
            "primary": "#FFFFFF",
            "secondary": "#AAAAAA",
            "background": "#000000",
            "highlight": "#FFFFFF",
            "text": "#FFFFFF"
        }
    }
    
    # Default to purple if color scheme not found
    colors = color_schemes.get(color_scheme.lower(), color_schemes["purple"])
    
    # Generate visualization based on type
    if visualization_type.lower() == "waveform":
        return generate_waveform_visualization(audio_id, colors)
    elif visualization_type.lower() == "spectrogram":
        return generate_spectrogram_visualization(audio_id, colors)
    elif visualization_type.lower() == "animated":
        return generate_animated_visualization(audio_id, colors)
    elif visualization_type.lower() == "circular":
        return generate_circular_visualization(audio_id, colors)
    elif visualization_type.lower() == "3d":
        return generate_3d_visualization(audio_id, colors)
    else:
        # Default to waveform
        return generate_waveform_visualization(audio_id, colors)


def generate_waveform_visualization(audio_id: str, colors: Dict[str, str]) -> Dict[str, Any]:
    """
    Generate a waveform visualization.
    
    Args:
        audio_id: Unique identifier for the audio
        colors: Color scheme to use
        
    Returns:
        Dictionary containing visualization data
    """
    # Generate a URL for the visualization
    url = f"/visualizations/waveform/{audio_id}_{colors['primary'].replace('#', '')}.png"
    
    # Generate a thumbnail URL
    thumbnail_url = f"/visualizations/waveform/thumbnails/{audio_id}_{colors['primary'].replace('#', '')}_thumb.png"
    
    # Generate mock waveform data
    waveform_data = []
    num_points = 100
    for i in range(num_points):
        # Generate a random amplitude between 0.1 and 1.0
        # With some patterns to make it look like a real waveform
        if i < num_points / 4:
            # Intro - gradually increasing
            amplitude = 0.1 + (i / (num_points / 4)) * 0.5
        elif i < num_points / 2:
            # First half - medium amplitude with variation
            amplitude = 0.6 + random.uniform(-0.2, 0.2)
        elif i < 3 * num_points / 4:
            # Second half - higher amplitude with variation
            amplitude = 0.8 + random.uniform(-0.3, 0.2)
        else:
            # Outro - gradually decreasing
            amplitude = 0.8 - ((i - 3 * num_points / 4) / (num_points / 4)) * 0.7
        
        waveform_data.append(max(0.05, min(1.0, amplitude)))
    
    return {
        "url": url,
        "thumbnail_url": thumbnail_url,
        "data": {
            "type": "waveform",
            "points": waveform_data,
            "colors": colors,
            "width": 800,
            "height": 200,
            "resolution": "high"
        }
    }


def generate_spectrogram_visualization(audio_id: str, colors: Dict[str, str]) -> Dict[str, Any]:
    """
    Generate a spectrogram visualization.
    
    Args:
        audio_id: Unique identifier for the audio
        colors: Color scheme to use
        
    Returns:
        Dictionary containing visualization data
    """
    # Generate a URL for the visualization
    url = f"/visualizations/spectrogram/{audio_id}_{colors['primary'].replace('#', '')}.png"
    
    # Generate a thumbnail URL
    thumbnail_url = f"/visualizations/spectrogram/thumbnails/{audio_id}_{colors['primary'].replace('#', '')}_thumb.png"
    
    # Generate mock spectrogram data
    spectrogram_data = []
    num_time_points = 50
    num_freq_bands = 30
    
    for t in range(num_time_points):
        time_slice = []
        for f in range(num_freq_bands):
            # Generate frequency intensity with patterns
            # Lower frequencies tend to have more energy
            base_intensity = max(0, 1.0 - (f / num_freq_bands) * 0.8)
            
            # Add time-based patterns
            if t < num_time_points / 4:
                # Intro - gradually increasing
                time_factor = t / (num_time_points / 4)
            elif t < num_time_points / 2:
                # First half - medium intensity
                time_factor = 0.7 + random.uniform(-0.1, 0.1)
            elif t < 3 * num_time_points / 4:
                # Second half - higher intensity
                time_factor = 0.9 + random.uniform(-0.1, 0.1)
            else:
                # Outro - gradually decreasing
                time_factor = 1.0 - ((t - 3 * num_time_points / 4) / (num_time_points / 4))
            
            # Add some random variation
            variation = random.uniform(-0.2, 0.2)
            
            # Calculate final intensity
            intensity = max(0, min(1.0, base_intensity * time_factor + variation))
            time_slice.append(intensity)
        
        spectrogram_data.append(time_slice)
    
    return {
        "url": url,
        "thumbnail_url": thumbnail_url,
        "data": {
            "type": "spectrogram",
            "time_points": num_time_points,
            "frequency_bands": num_freq_bands,
            "intensities": spectrogram_data,
            "colors": colors,
            "width": 800,
            "height": 400,
            "resolution": "high"
        }
    }


def generate_animated_visualization(audio_id: str, colors: Dict[str, str]) -> Dict[str, Any]:
    """
    Generate an animated visualization.
    
    Args:
        audio_id: Unique identifier for the audio
        colors: Color scheme to use
        
    Returns:
        Dictionary containing visualization data
    """
    # Generate URLs for the visualization
    url = f"/visualizations/animated/{audio_id}_{colors['primary'].replace('#', '')}.png"
    animated_url = f"/visualizations/animated/{audio_id}_{colors['primary'].replace('#', '')}.gif"
    
    # Generate a thumbnail URL
    thumbnail_url = f"/visualizations/animated/thumbnails/{audio_id}_{colors['primary'].replace('#', '')}_thumb.png"
    
    # Generate mock animation data
    animation_frames = 30
    particles = 50
    
    # Generate particle data
    particle_data = []
    for p in range(particles):
        # Initial position and velocity
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        vx = random.uniform(-0.02, 0.02)
        vy = random.uniform(-0.02, 0.02)
        size = random.uniform(0.01, 0.05)
        
        # Track position over frames
        positions = []
        for f in range(animation_frames):
            # Update position
            x += vx
            y += vy
            
            # Bounce off edges
            if x < 0 or x > 1:
                vx = -vx
                x = max(0, min(1, x))
            if y < 0 or y > 1:
                vy = -vy
                y = max(0, min(1, y))
            
            # Add some random variation
            vx += random.uniform(-0.005, 0.005)
            vy += random.uniform(-0.005, 0.005)
            
            # Limit velocity
            vx = max(-0.05, min(0.05, vx))
            vy = max(-0.05, min(0.05, vy))
            
            # Record position
            positions.append({"x": x, "y": y, "size": size})
        
        particle_data.append(positions)
    
    return {
        "url": url,
        "animated_url": animated_url,
        "thumbnail_url": thumbnail_url,
        "data": {
            "type": "animated",
            "frames": animation_frames,
            "particles": particles,
            "particle_data": particle_data,
            "colors": colors,
            "width": 800,
            "height": 800,
            "fps": 30,
            "resolution": "high"
        }
    }


def generate_circular_visualization(audio_id: str, colors: Dict[str, str]) -> Dict[str, Any]:
    """
    Generate a circular visualization.
    
    Args:
        audio_id: Unique identifier for the audio
        colors: Color scheme to use
        
    Returns:
        Dictionary containing visualization data
    """
    # Generate a URL for the visualization
    url = f"/visualizations/circular/{audio_id}_{colors['primary'].replace('#', '')}.png"
    
    # Generate a thumbnail URL
    thumbnail_url = f"/visualizations/circular/thumbnails/{audio_id}_{colors['primary'].replace('#', '')}_thumb.png"
    
    # Generate mock circular data
    num_segments = 36
    num_rings = 5
    
    # Generate segment data
    segment_data = []
    for r in range(num_rings):
        ring = []
        for s in range(num_segments):
            # Generate intensity with patterns
            # Outer rings tend to have less intensity
            base_intensity = max(0, 1.0 - (r / num_rings) * 0.5)
            
            # Add segment-based patterns
            segment_factor = 0.5 + 0.5 * abs(math.sin(s * math.pi / 6))
            
            # Add some random variation
            variation = random.uniform(-0.2, 0.2)
            
            # Calculate final intensity
            intensity = max(0, min(1.0, base_intensity * segment_factor + variation))
            ring.append(intensity)
        
        segment_data.append(ring)
    
    return {
        "url": url,
        "thumbnail_url": thumbnail_url,
        "data": {
            "type": "circular",
            "segments": num_segments,
            "rings": num_rings,
            "intensities": segment_data,
            "colors": colors,
            "width": 800,
            "height": 800,
            "resolution": "high"
        }
    }


def generate_3d_visualization(audio_id: str, colors: Dict[str, str]) -> Dict[str, Any]:
    """
    Generate a 3D visualization.
    
    Args:
        audio_id: Unique identifier for the audio
        colors: Color scheme to use
        
    Returns:
        Dictionary containing visualization data
    """
    # Generate URLs for the visualization
    url = f"/visualizations/3d/{audio_id}_{colors['primary'].replace('#', '')}.png"
    animated_url = f"/visualizations/3d/{audio_id}_{colors['primary'].replace('#', '')}.gif"
    
    # Generate a thumbnail URL
    thumbnail_url = f"/visualizations/3d/thumbnails/{audio_id}_{colors['primary'].replace('#', '')}_thumb.png"
    
    # Generate mock 3D data
    grid_size = 20
    
    # Generate height map data
    height_map = []
    for x in range(grid_size):
        row = []
        for z in range(grid_size):
            # Generate height with patterns
            # Center tends to have more height
            distance_from_center = math.sqrt((x - grid_size/2)**2 + (z - grid_size/2)**2) / (grid_size/2)
            base_height = max(0, 1.0 - distance_from_center * 0.8)
            
            # Add some terrain-like patterns
            terrain_factor = 0.5 + 0.5 * (math.sin(x * 0.5) + math.cos(z * 0.5))
            
            # Add some random variation
            variation = random.uniform(-0.2, 0.2)
            
            # Calculate final height
            height = max(0, min(1.0, base_height * terrain_factor + variation))
            row.append(height)
        
        height_map.append(row)
    
    return {
        "url": url,
        "animated_url": animated_url,
        "thumbnail_url": thumbnail_url,
        "data": {
            "type": "3d",
            "grid_size": grid_size,
            "height_map": height_map,
            "colors": colors,
            "width": 800,
            "height": 800,
            "resolution": "high"
        }
    }


# Import math for circular and 3D visualizations
import math 