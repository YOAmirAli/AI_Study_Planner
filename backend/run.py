import os
from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Get port from environment or default to 10000
    port = int(os.getenv('PORT', 10000))
    
    # Run the application
    print(f"Starting AI Study Planner API on http://0.0.0.0:{port}")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Health check available at: http://0.0.0.0:{port}/api/health")
    
    app.run(
        host='0.0.0.0',
        port=port
    )
