#!/usr/bin/env python3
"""
Sample test file created for demonstration purposes.
"""

import unittest

class SampleTestCase(unittest.TestCase):
    """A simple test case to demonstrate basic testing."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_data = [1, 2, 3, 4, 5]
    
    def test_list_length(self):
        """Test that our test data has the expected length."""
        self.assertEqual(len(self.test_data), 5)
    
    def test_list_contents(self):
        """Test that our test data contains expected values."""
        self.assertIn(3, self.test_data)
        self.assertNotIn(6, self.test_data)
    
    def test_list_sum(self):
        """Test that the sum of our test data is correct."""
        self.assertEqual(sum(self.test_data), 15)
    
    def test_always_passes(self):
        """A test that always passes."""
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()