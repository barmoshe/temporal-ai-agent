import unittest
import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tools.midi_creation_tool import midi_creation_tool

class TestMidiCreationTool(unittest.TestCase):
    """Test cases for the MidiCreationTool."""

    def test_valid_input(self):
        """Test with valid input."""
        test_input = {
            "music_text": [
                [60, 0.25],  # Middle C with a duration of a sixteenth note
                [0, 0.25],   # Silence for a sixteenth note
                [62, 0.5]    # D with a duration of an eighth note
            ]
        }
        result = midi_creation_tool(test_input)
        self.assertEqual(result["status"], "success")
        self.assertIn("result", result)
        self.assertIsInstance(result["result"], list)
        # Should contain 5 messages: note_on, note_off, delay, note_on, note_off
        self.assertEqual(len(result["result"]), 5)
    
    def test_missing_music_text(self):
        """Test handling when 'music_text' is missing."""
        result = midi_creation_tool({})
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)
        self.assertIn("Missing 'music_text'", result["error"])
    
    def test_invalid_tuple_format(self):
        """Test handling of invalid tuple format."""
        test_input = {"music_text": ["invalid", 0.5]}
        result = midi_creation_tool(test_input)
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)
        self.assertIn("Invalid format", result["error"])
    
    def test_invalid_note_value(self):
        """Test invalid note value."""
        test_input = {"music_text": [[10, 0.5]]}  # 10 is invalid
        result = midi_creation_tool(test_input)
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)
        self.assertIn("Invalid note", result["error"])
    
    def test_invalid_duration_value(self):
        """Test invalid duration value."""
        test_input = {"music_text": [[60, 3.0]]}  # 3.0 is greater than max allowed duration
        result = midi_creation_tool(test_input)
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)
        self.assertIn("Invalid duration", result["error"])
    
    def test_empty_music_text(self):
        """Test with empty music_text list."""
        test_input = {"music_text": []}
        result = midi_creation_tool(test_input)
        self.assertEqual(result["status"], "success")
        self.assertIn("result", result)
        self.assertEqual(len(result["result"]), 0)
    
    def test_single_note(self):
        """Test with a single note."""
        test_input = {"music_text": [[60, 1.0]]}  # Middle C with a duration of a quarter note
        result = midi_creation_tool(test_input)
        self.assertEqual(result["status"], "success")
        self.assertIn("result", result)
        self.assertEqual(len(result["result"]), 2)  # note_on and note_off
    
    def test_single_silence(self):
        """Test with a single silence."""
        test_input = {"music_text": [[0, 1.0]]}  # Silence for a quarter note
        result = midi_creation_tool(test_input)
        self.assertEqual(result["status"], "success")
        self.assertIn("result", result)
        self.assertEqual(len(result["result"]), 1)  # Only a delay message

if __name__ == "__main__":
    unittest.main() 