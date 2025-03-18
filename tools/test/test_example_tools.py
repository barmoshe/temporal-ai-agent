"""
Test Example Tools

This module provides unit tests for the example tools.
"""
import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tools.example_tool_class import example_tool_class
from tools.example_tool_function import example_tool_function


class TestExampleTools(unittest.TestCase):
    """Test case for example tools."""
    
    def test_example_tool_class(self):
        """Test the class-based example tool."""
        # Test with default message
        result = example_tool_class({})
        self.assertEqual(result["greeting"], "Hello, World!")
        self.assertEqual(result["original_message"], "World")
        self.assertEqual(result["status"], "success")
        
        # Test with custom message
        result = example_tool_class({"message": "Developer"})
        self.assertEqual(result["greeting"], "Hello, Developer!")
        self.assertEqual(result["original_message"], "Developer")
        self.assertEqual(result["status"], "success")
    
    def test_example_tool_function(self):
        """Test the function-based example tool."""
        # Test with default message
        result = example_tool_function({})
        self.assertEqual(result["farewell"], "Goodbye, World!")
        self.assertEqual(result["original_message"], "World")
        self.assertEqual(result["status"], "success")
        
        # Test with custom message
        result = example_tool_function({"message": "Developer"})
        self.assertEqual(result["farewell"], "Goodbye, Developer!")
        self.assertEqual(result["original_message"], "Developer")
        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main() 