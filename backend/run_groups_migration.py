"""
Script to create groups tables in the database
Run this before using the groups feature
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migration():
    """Run the groups tables migration"""
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'vp-project')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("Connected to MySQL database")
            print("Running groups tables migration...")
            
            # Read the migration file
            with open('migrations/create_groups_tables.sql', 'r', encoding='utf-8') as file:
                sql_script = file.read()
            
            # Split by semicolon and execute each statement
            statements = sql_script.split(';')
            
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                        print(f"✓ Executed: {statement[:50]}...")
                    except Error as e:
                        print(f"✗ Error executing statement: {e}")
                        print(f"  Statement: {statement[:100]}...")
            
            connection.commit()
            
            # Verify tables were created
            cursor.execute("""
                SELECT TABLE_NAME, TABLE_ROWS 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME IN ('groups', 'group_members')
            """, (os.getenv('DB_NAME', 'vp-project'),))
            
            tables = cursor.fetchall()
      