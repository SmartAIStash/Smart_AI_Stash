import unittest
import sqlite3
from unittest.mock import patch, MagicMock
import datetime

class DatabaseTest(unittest.TestCase):
    """Advanced test suite for database operations with comprehensive testing"""
    
    def setUp(self):
        """Set up test database connection"""
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        
        # Create comprehensive test tables
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                age INTEGER
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.connection.commit()
        
    def tearDown(self):
        """Clean up database connection"""
        self.connection.close()
        
    def test_advanced_user_operations(self):
        """Test complex user database operations"""
        # Insert multiple users with different data
        users = [
            ("Alice Cooper", "alice@example.com", 28, 1),
            ("Bob Dylan", "bob@example.com", 35, 1),
            ("Charlie Parker", "charlie@example.com", 42, 0),
            ("Diana Ross", "diana@example.com", 31, 1)
        ]
        
        self.cursor.executemany(
            "INSERT INTO users (name, email, age, is_active) VALUES (?, ?, ?, ?)", 
            users
        )
        self.connection.commit()
        
        # Test complex queries
        # Active users only
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
        active_count = self.cursor.fetchone()[0]
        self.assertEqual(active_count, 3)
        
        # Users above certain age
        self.cursor.execute("SELECT name FROM users WHERE age > 30 ORDER BY age DESC")
        older_users = self.cursor.fetchall()
        self.assertEqual(len(older_users), 3)
        self.assertEqual(older_users[0][0], "Charlie Parker")  # Oldest first
        
    def test_user_post_relationships(self):
        """Test foreign key relationships and joins"""
        # Insert a user
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("John Doe", "john@example.com", 30)
        )
        user_id = self.cursor.lastrowid
        
        # Insert posts for this user
        posts = [
            (user_id, "First Post", "This is my first post content"),
            (user_id, "Second Post", "This is my second post content"),
            (user_id, "Third Post", "This is my third post content")
        ]
        
        self.cursor.executemany(
            "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
            posts
        )
        self.connection.commit()
        
        # Test JOIN query
        self.cursor.execute('''
            SELECT u.name, COUNT(p.id) as post_count
            FROM users u
            LEFT JOIN posts p ON u.id = p.user_id
            WHERE u.id = ?
            GROUP BY u.id, u.name
        ''', (user_id,))
        
        result = self.cursor.fetchone()
        self.assertEqual(result[0], "John Doe")
        self.assertEqual(result[1], 3)  # Should have 3 posts
        
    def test_database_transactions(self):
        """Test database transaction handling"""
        try:
            # Start transaction
            self.cursor.execute("BEGIN TRANSACTION")
            
            # Insert user
            self.cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                ("Transaction User", "trans@example.com")
            )
            
            # Simulate an error condition
            user_id = self.cursor.lastrowid
            
            # This should work
            self.cursor.execute(
                "INSERT INTO posts (user_id, title) VALUES (?, ?)",
                (user_id, "Test Post")
            )
            
            # Commit transaction
            self.connection.commit()
            
            # Verify data was saved
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE name = ?", ("Transaction User",))
            user_count = self.cursor.fetchone()[0]
            self.assertEqual(user_count, 1)
            
        except Exception as e:
            # Rollback on error
            self.connection.rollback()
            self.fail(f"Transaction failed: {e}")
            
    def test_data_validation_and_constraints(self):
        """Test database constraints and validation"""
        # Test unique constraint
        self.cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            ("User One", "unique@example.com")
        )
        
        # This should fail due to unique constraint
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                ("User Two", "unique@example.com")  # Same email
            )
            
    def test_database_performance_queries(self):
        """Test database performance with larger datasets"""
        # Insert many users for performance testing
        large_dataset = [
            (f"User {i}", f"user{i}@example.com", 20 + (i % 50), i % 2)
            for i in range(100)
        ]
        
        self.cursor.executemany(
            "INSERT INTO users (name, email, age, is_active) VALUES (?, ?, ?, ?)",
            large_dataset
        )
        self.connection.commit()
        
        # Test complex aggregation query
        self.cursor.execute('''
            SELECT 
                is_active,
                COUNT(*) as user_count,
                AVG(age) as avg_age,
                MIN(age) as min_age,
                MAX(age) as max_age
            FROM users 
            GROUP BY is_active
            ORDER BY is_active DESC
        ''')
        
        results = self.cursor.fetchall()
        self.assertEqual(len(results), 2)  # Should have 2 groups (active/inactive)
        
        # Verify we have the expected number of users
        total_users = sum(result[1] for result in results)
        self.assertEqual(total_users, 100)

if __name__ == '__main__':
    unittest.main()