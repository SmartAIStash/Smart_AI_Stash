#!/usr/bin/env python3
"""
EDITED VERSION - Advanced test file with string operations
"""
import unittest
import re

class AdvancedStringTest(unittest.TestCase):
    """Advanced test class for string operations - EDITED VERSION"""
    
    def setUp(self):
        """Set up test data for string operations"""
        self.test_string = "Hello, World! This is a test string."
        self.numbers_string = "12345"
        self.mixed_string = "Test123String456"
    
    def test_string_length(self):
        """Test string length calculation"""
        self.assertEqual(len(self.test_string), 37)
        self.assertEqual(len(self.numbers_string), 5)
    
    def test_string_case_conversion(self):
        """Test string case conversions"""
        self.assertEqual(self.test_string.upper(), "HELLO, WORLD! THIS IS A TEST STRING.")
        self.assertEqual(self.test_string.lower(), "hello, world! this is a test string.")
    
    def test_string_contains(self):
        """Test string contains operations"""
        self.assertIn("Hello", self.test_string)
        self.assertIn("World", self.test_string)
        self.assertNotIn("Python", self.test_string)
    
    def test_string_split(self):
        """Test string splitting"""
        words = self.test_string.split()
        self.assertEqual(len(words), 7)
        self.assertEqual(words[0], "Hello,")
        self.assertEqual(words[1], "World!")
    
    def test_digit_extraction(self):
        """Test extracting digits from strings"""
        digits = re.findall(r'\d+', self.mixed_string)
        self.assertEqual(digits, ['123', '456'])
    
    def test_string_replacement(self):
        """Test string replacement"""
        replaced = self.test_string.replace("World", "Python")
        self.assertEqual(replaced, "Hello, Python! This is a test string.")
    
    def test_string_starts_ends(self):
        """Test string starts and ends with"""
        self.assertTrue(self.test_string.startswith("Hello"))
        self.assertTrue(self.test_string.endswith("string."))
        self.assertFalse(self.test_string.startswith("Python"))

if __name__ == '__main__':
    print("Running EDITED version of the test suite...")
    unittest.main()