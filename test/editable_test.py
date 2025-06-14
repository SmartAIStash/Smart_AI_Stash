#!/usr/bin/env python3
"""
Initial test file - to be edited later
"""
import unittest

class InitialTest(unittest.TestCase):
    """Basic initial test class"""
    
    def setUp(self):
        """Set up test data"""
        self.numbers = [1, 2, 3]
    
    def test_basic_addition(self):
        """Test basic addition"""
        result = sum(self.numbers)
        self.assertEqual(result, 6)
    
    def test_list_length(self):
        """Test list length"""
        self.assertEqual(len(self.numbers), 3)

if __name__ == '__main__':
    unittest.main()