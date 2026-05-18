import os
from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Run the application
    print(f"Starting AI Study Planner API on http://localhost:{port}")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Health check available at: http://localhost:{port}/api/health")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
