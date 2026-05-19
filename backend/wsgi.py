"""WSGI entry point for production (Gunicorn, Render, etc.)."""
from app import create_app

app = create_app()
