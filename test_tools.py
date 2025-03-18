#!/usr/bin/env python3
"""
Tool Tests

This module provides unit tests for the tools in the system.
"""
import unittest
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