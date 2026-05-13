"""
Fix Duplicate group_messages Tables
This script removes duplicate tables and recreates them with correct structure
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fix_duplicate_tables():
    """Fix duplicate group_messages tables"""
    try:
        # Database connection
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'vp-project')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            print("=" * 80)
            print("Connected to MySQL database")
            print("=" * 80)
            
            # Step 1: Check for duplicate tables
            print("\n1. Checking for duplicate tables...")
            cursor.execute("""
                SELECT TABLE_NAME, TABLE_SCHEMA 
                FROM information_schema.TABLES 
                WHERE TABLE_NAME LIKE '%group_message%' 
                AND TABLE_SCHEMA = %s
            """, (os.getenv('DB_NAME', 'vp-project'),))
            
            existing_tables = cursor.fetchall()
            print(f"   Found {len(existing_tables)} table(s):")
            for table in existing_tables:
                print(f"   - {table[0]}")
            
            # Step 2: Ask for confirmation
            print("\n⚠️  WARNING: This will delete all existing group messages!")
            response = input("   Do you want to continue? (yes/no): ")
            
            if response.lower() != 'yes':
                print("   Operation cancelled.")
                return False
            
            # Step 3: Drop existing tables
            print("\n2. Dropping existing tables...")
            try:
                cursor.execute("DROP TABLE IF EXISTS group_message_reads")
                print("   ✓ Dropped group_message_reads (if existed)")
            except Error as e:
                print(f"   ⚠ Error dropping group_message_reads: {e}")
            
            try:
                cursor.execute("DROP TABLE IF EXISTS group_messages")
                print("   ✓ Dropped group_messages (if existed)")
            except Error as e:
                print(f"   ⚠ Error dropping group_messages: {e}")
            
            connection.commit()
            
            # Step 4: Create group_messages table
            print("\n3. Creating group_messages table...")
            cursor.execute("""
                CREATE TABLE group_messages (
                    message_id INT AUTO_INCREMENT PRIMARY KEY,
                    group_id INT NOT NULL,
                    user_id INT NOT NULL,
                    message_text TEXT NOT NULL,
                    message_type VARCHAR(20) DEFAULT 'text' NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    edited_at TIMESTAMP NULL DEFAULT NULL,
                    
                    INDEX idx_group_messages_group_id (group_id),
                    INDEX idx_group_messages_user_id (user_id),
                    INDEX idx_group_messages_created_at (created_at),
                    
                    FOREIGN KEY (group_id) REFERENCES `groups`(group_id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("   ✓ Created group_messages table")
            
            # Step 5: Create group_message_reads table
            print("\n4. Creating group_message_reads table...")
            cursor.execute("""
                CREATE TABLE group_message_reads (
                    message_id INT NOT NULL,
                    user_id INT NOT NULL,
                    read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    
                    PRIMARY KEY (message_id, user_id),
                    INDEX idx_message_reads_user (user_id),
                    INDEX idx_message_reads_read_at (read_at),
                    
                    FOREIGN KEY (message_id) REFERENCES group_messages(message_id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("   ✓ Created group_message_reads table")
            
            connection.commit()
            
            # Step 6: Verify tables
            print("\n5. Verifying tables...")
            cursor.execute("""
                SELECT TABLE_NAME, TABLE_ROWS, CREATE_TIME
                FROM information_schema.TABLES 
                WHERE TABLE_NAME IN ('group_messages', 'group_message_re