"""
Logging Configuration for CloudOps Ninja

This module provides structured logging for the Flask application with:
- Configurable log levels (DEBUG, INFO, WARNING, ERROR)
- Console and file logging
- Structured log formatting
- Request/response logging for Flask endpoints
"""

import logging
import logging.handlers
import os
from datetime import datetime


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'
    }
    
    def __init__(self, use_color=True):
        self.use_color = use_color
        super().__init__()
    
    def format(self, record):
        """Format log record with color and structure"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        level_name = record.levelname
        
        # Add color if enabled and not in file
        if self.use_color:
            color = self.COLORS.get(level_name, self.COLORS['RESET'])
            reset = self.COLORS['RESET']
            level_name = f"{color}{level_name}{reset}"
        
        # Build the formatted message
        message = f"[{timestamp}] {level_name:20} | {record.name:30} | {record.getMessage()}"
        
        # Add exception info if present
        if record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"
        
        return message


def get_log_level(level_name: str = None) -> int:
    """
    Get logging level from environment or parameter
    
    Args:
        level_name: Optional log level name (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        logging level constant
    """
    if level_name is None:
        level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    return level_map.get(level_name, logging.INFO)


def configure_logging(app=None, log_level: str = None, log_file: str = None):
    """
    Configure logging for the application
    
    Args:
        app: Flask application instance (optional)
        log_level: Log level to use (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file (optional)
    """
    # Get log level from parameter or environment
    log_level = get_log_level(log_level)
    
    # Create logs directory if needed
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Console handler with color formatting
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = StructuredFormatter(use_color=True)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_formatter = StructuredFormatter(use_color=False)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Configure Flask app logger if provided
    if app:
        app.logger.setLevel(log_level)
        
        # Remove default Flask handler
        app.logger.handlers = []
        
        # Add our handlers
        for handler in root_logger.handlers:
            app.logger.addHandler(handler)
    
    return root_logger


def get_logger(name: str):
    """
    Get a logger instance for a module
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        logging.Logger instance
    """
    return logging.getLogger(name)


class RequestLogger:
    """Middleware for logging HTTP requests and responses"""
    
    def __init__(self, app=None):
        self.app = app
        self.logger = get_logger(__name__)
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        @app.before_request
        def log_request():
            from flask import request
            self.logger.debug(
                f"Request started: {request.method} {request.path}",
                extra={
                    'remote_addr': request.remote_addr,
                    'user_agent': request.user_agent
                }
            )
        
        @app.after_request
        def log_response(response):
            from flask import request
            self.logger.debug(
                f"Request completed: {request.method} {request.path} - Status: {response.status_code}",
                extra={
                    'status_code': response.status_code,
                    'content_length': response.content_length
                }
            )
            return response
    
    def log_request_start(self, method, path, remote_addr=None):
        """Log the start of a request"""
        self.logger.debug(f"Request started: {method} {path}", extra={
            'remote_addr': remote_addr
        })
    
    def log_request_end(self, method, path, status_code):
        """Log the end of a request"""
        self.logger.debug(f"Request completed: {method} {path} - Status: {status_code}", extra={
            'status_code': status_code
        })
    
    def log_request_error(self, method, path, error):
        """Log a request error"""
        self.logger.error(f"Request error: {method} {path} - {str(error)}", exc_info=True)


# Module-level logger
logger = get_logger(__name__)


def log_database_operation(operation: str, entity: str, details: dict = None):
    """
    Log database operations
    
    Args:
        operation: Type of operation (CREATE, READ, UPDATE, DELETE)
        entity: Entity being operated on
        details: Optional details dictionary
    """
    logger.info(f"Database {operation}: {entity}", extra=details or {})


def log_authentication(username: str, success: bool, error: str = None):
    """
    Log authentication attempts
    
    Args:
        username: Username attempting authentication
        success: Whether authentication succeeded
        error: Optional error message
    """
    if success:
        logger.info(f"Authentication successful for user: {username}")
    else:
        logger.warning(f"Authentication failed for user: {username} - Error: {error}")


def log_deployment(cloud: str, version: str, status: str):
    """
    Log deployment events
    
    Args:
        cloud: Cloud provider (aws, gcp)
        version: Version deployed
        status: Deployment status (success, failed)
    """
    logger.info(f"Deployment to {cloud} (version {version}): {status}")


def log_health_check_result(overall_status: str, checks_summary: dict):
    """
    Log health check results
    
    Args:
        overall_status: Overall health status
        checks_summary: Summary of individual checks
    """
    logger.info(
        f"Health check completed: {overall_status}",
        extra={
            'healthy': checks_summary.get('healthy', 0),
            'degraded': checks_summary.get('degraded', 0),
            'unhealthy': checks_summary.get('unhealthy', 0)
        }
    )
