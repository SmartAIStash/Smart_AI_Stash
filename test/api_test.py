import unittest
import requests
from unittest.mock import patch, Mock
import json

class APITest(unittest.TestCase):
    """Test suite for API operations"""
    
    def setUp(self):
        """Set up test configuration"""
        self.base_url = "https://api.example.com"
        self.headers = {"Content-Type": "application/json"}
        self.test_data = {
            "name": "Test User",
            "email": "test@example.com",
            "age": 25
        }
    
    @patch('requests.get')
    def test_get_request(self, mock_get):
        """Test GET request functionality"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "name": "John Doe"}
        mock_get.return_value = mock_response
        
        # Make request
        response = requests.get(f"{self.base_url}/users/1")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("name", data)
        self.assertEqual(data["name"], "John Doe")
        
    @patch('requests.post')
    def test_post_request(self, mock_post):
        """Test POST request functionality"""
        # Mock successful creation response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 2, **self.test_data}
        mock_post.return_value = mock_response
        
        # Make request
        response = requests.post(
            f"{self.base_url}/users",
            headers=self.headers,
            data=json.dumps(self.test_data)
        )
        
        # Assertions
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], self.test_data["name"])
        self.assertEqual(data["email"], self.test_data["email"])
        
    @patch('requests.put')
    def test_put_request(self, mock_put):
        """Test PUT request functionality"""
        updated_data = {**self.test_data, "age": 26}
        
        # Mock successful update response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, **updated_data}
        mock_put.return_value = mock_response
        
        # Make request
        response = requests.put(
            f"{self.base_url}/users/1",
            headers=self.headers,
            data=json.dumps(updated_data)
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["age"], 26)
        
    @patch('requests.delete')
    def test_delete_request(self, mock_delete):
        """Test DELETE request functionality"""
        # Mock successful deletion response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response
        
        # Make request
        response = requests.delete(f"{self.base_url}/users/1")
        
        # Assertions
        self.assertEqual(response.status_code, 204)
        
    @patch('requests.get')
    def test_error_handling(self, mock_get):
        """Test API error handling"""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "User not found"}
        mock_get.return_value = mock_response
        
        # Make request
        response = requests.get(f"{self.base_url}/users/9999")
        
        # Assertions
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("error", data)

if __name__ == '__main__':
    unittest.main()