class AppError(Exception):
    """Base application exception."""
    pass
class FileNotFoundError(AppError):
    pass
class InvalidPathError(AppError):
    pass
class ExtractionError(AppError):
    pass