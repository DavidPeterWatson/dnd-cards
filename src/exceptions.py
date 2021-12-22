class Error(Exception):
    """Raised when sm cli generates an error"""
    pass

class ConfigError(Error):
    """Raised when config generates error"""
    pass