class AppError(Exception):
    """Base application exception."""
    pass
class FileNotFoundError(AppError):
    pass
class InvalidPathError(AppError):
    pass
class InvalidDocumentError(AppError):
    pass
class ExtractionError(AppError):
    pass
class IndexingError(AppError):
    pass
class VectorStoreError(AppError):
    pass