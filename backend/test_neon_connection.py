import os
import sys
from dotenv import load_dotenv
import psycopg2

def test_neon_connection():
    """Test connection to Neon database"""
    
    print("=" * 60)
    print("Testing Neon Database Connection")
    print("=" * 60)
    
    # Load environment variables from .env file
    env_path = ".env"
    if not os.path.exists(env_path):
        print(f"? ERROR: {env_path} file not found in current directory")
        print(f"Current directory: {os.getcwd()}")
        return False
    
    print(f"? Found {env_path} file")
    load_dotenv(env_path)
    
    # Get DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("? ERROR: DATABASE_URL not found in .env file")
        return False
    
    print("? DATABASE_URL loaded from .env")
    print(f"  Connecting to: {database_url[:50]}..." if len(database_url) > 50 else f"  Connecting to: {database_url}")
    
    try:
        # Attempt to connect to the database
        print("\nAttempting to connect...")
        conn = psycopg2.connect(database_url)
        
        # Test the connection by running a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("? Successfully connected to Neon database!")
        print(f"  PostgreSQL version: {version[0]}")
        
        # Get connection info
        print(f"\n  Connection Details:")
        print(f"  - Host: {conn.info.host}")
        print(f"  - Port: {conn.info.port}")
        print(f"  - Database: {conn.info.dbname}")
        print(f"  - User: {conn.info.user}")
        print(f"  - Status: {conn.status}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("? Connection test PASSED")
        print("=" * 60)
        return True
        
    except psycopg2.OperationalError as e:
        print(f"? Connection failed (Operational Error)")
        print(f"   Error: {str(e)}")
        return False
    except psycopg2.ProgrammingError as e:
        print(f"? Connection failed (Programming Error)")
        print(f"   Error: {str(e)}")
        return False
    except Exception as e:
        print(f"? Connection failed (Unexpected Error)")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_neon_connection()
    sys.exit(0 if success else 1)
