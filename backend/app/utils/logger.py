"""
Logging Configuration
Centralized logging setup for the application
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(app):
    """
    Configure application logging
    
    Args:
        app: Flask application instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set log level based on environment
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # File handler for general logs
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # File handler for error logs
    error_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Configure app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # Log startup
    app.logger.info('='*60)
    app.logger.info('AI Study Planner API Starting')
    app.logger.info(f'Environment: {app.config.get("ENV")}')
    app.logger.info(f'Debug Mode: {app.config.get("DEBUG")}')
    app.logger.info(f'Log Level: {logging.getLevelName(log_level)}')
    app.logger.info('='*60)
    
    return app.logger

def log_request(request, response_status, response_time):
    """
    Log HTTP request details
    
    Args:
        request: Flask request object
        response_status: HTTP status code
        response_time: Response time in milliseconds
    """
    from flask import current_app
    
    current_app.logger.info(
        f'{request.method} {request.path} - '
        f'Status: {response_status} - '
        f'Time: {response_time:.2f}ms - '
        f'IP: {request.remote_addr}'
    )

def log_error(error, context=None):
    """
    Log error with context
    
    Args:
        error: Exception object
        context: Additional context information
    """
    from flask import current_app
    
    error_msg = f'Error: {str(error)}'
    if context:
        error_msg += f' | Context: {context}'
    
    current_app.logger.error(error_msg, exc_info=True)

def log_database_query(query, execution_time):
    """
    Log slow database queries
    
    Args:
        query: SQL query string
        execution_time: Query execution time in milliseconds
    """
    from flask import current_app
    
    # Log queries that take longer than 100ms
    if execution_time > 100:
        current_app.logger.warning(
            f'Slow Query ({execution_time:.2f}ms): {query[:200]}'
        )
