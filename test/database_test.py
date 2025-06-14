import unittest
import sqlite3
from unittest.mock import patch, MagicMock

class DatabaseTest(unittest.TestCase):
    """Test suite for database operations"""
    
    def setUp(self):
        """Set up test database connection"""
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        
    def tearDown(self):
        """Clean up database connection"""
        self.connection.close()
        
    def test_create_table(self):
        """Test table creation"""
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        ''')
        self.connection.commit()
        
        # Verify table was created
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'users')
        
    def test_insert_user(self):
        """Test user insertion"""
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        ''')
        
        # Insert test user
        self.cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                          ("John Doe", "john@example.com"))
        self.connection.commit()
        
        # Verify insertion
        self.cursor.execute("SELECT * FROM users WHERE name = ?", ("John Doe",))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "John Doe")
        self.assertEqual(user[2], "john@example.com")
        
    def test_query_users(self):
        """Test user queries"""
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        ''')
        
        # Insert multiple users
        users = [
            ("Alice Smith", "alice@example.com"),
            ("Bob Johnson", "bob@example.com"),
            ("Charlie Brown", "charlie@example.com")
        ]
        
        self.cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)
        self.connection.commit()
        
        # Test query all users
        self.cursor.execute("SELECT * FROM users")
        all_users = self.cursor.fetchall()
        self.assertEqual(len(all_users), 3)

if __name__ == '__main__':
    unittest.main()