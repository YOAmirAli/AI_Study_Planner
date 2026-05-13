"""
Run the join_code migration for groups table
This script adds the join_code column to the groups table
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migration():
    """Run the join_code migration"""
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
            print("Connected to MySQL database")
            
            # Read migration file
            with open('migrations/add_join_code_to_groups.sql', 'r') as file:
                sql_script = file.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement.upper().startswith('USE'):
                    continue  # Skip USE statement as we're already connected
                
                try:
                    cursor.execute(statement)
                    print(f"✓ Executed: {statement[:50]}...")
                except Error as e:
                    if 'Duplicate column name' in str(e):
                        print(f"⚠ Column already exists, skipping...")
                    elif 'Duplicate key name' in str(e):
                        print(f"⚠ Index already exists, skipping...")
                    else:
                        print(f"✗ Error: {e}")
                        raise
            
            connection.commit()
            print("\n✓ Migration completed successfully!")
            
            # Show the updated table structure
            cursor.execute("DESCRIBE `groups`")
            columns = cursor.fetchall()
            print("\nUpdated groups table structure:")
            print("-" * 80)
            for col in columns:
                print(f"{col[0]:20} {col[1]:20} {col[2]:10} {col[3]:10}")
            
    except Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection closed")
    
    return True

if __name__ == "__main__":
    print("=" * 80)
    print("Running join_code Migration for Groups Table")
    print("=" * 80)
    run_migration()
