"""
Quick script to verify quiz tables exist in database
Run this from backend directory: python verify_quiz_tables.py
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def verify_tables():
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'vp-project')
        )
        
        cursor = conn.cursor()
        
        # Check for quiz tables
        tables_to_check = ['quizzes', 'quiz_questions', 'quiz_results']
        
        print("=" * 50)
        print("QUIZ TABLES VERIFICATION")
        print("=" * 50)
        
        for table in tables_to_check:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            result = cursor.fetchone()
            
            if result:
                print(f"✅ Table '{table}' exists")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   └─ Contains {count} rows")
            else:
                print(f"❌ Table '{table}' NOT FOUND")
                print(f"   └─ Run: mysql -u root -p vp-project < migrations/add_quizzes_tables_mysql.sql")
        
        print("=" * 50)
        
        # Check recent quizzes
        cursor.execute("""
            SELECT quiz_id, title, status, total_questions, created_at 
            FROM quizzes 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        
        quizzes = cursor.fetchall()
        
        if quizzes:
            print("\nRECENT QUIZZES:")
            print("-" * 50)
            for quiz in quizzes:
                print(f"ID: {quiz[0]} | {quiz[1]} | Status: {quiz[2]} | Questions: {quiz[3]}")
        else:
            print("\nNo quizzes found in database.")
            print("Generate a quiz by completing a task!")
        
        print("=" * 50)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database Error: {e}")
        print("\nMake sure:")
        print("1. MySQL is running")
        print("2. Database 'vp-project' exists")
        print("3. .env file has correct credentials")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    verify_tables()
