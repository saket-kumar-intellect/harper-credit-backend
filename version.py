import os

def get_version():
    """Get version from environment variable or return default."""
    return os.getenv('VERSION', '1.0.0')

def get_commit():
    """Get commit hash from environment variable or return default."""
    return os.getenv('COMMIT', 'unknown')
