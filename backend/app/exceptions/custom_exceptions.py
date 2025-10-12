"""Custom exceptions for BuildFlow application"""


class BuildFlowException(Exception):
    """Base exception for BuildFlow"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResourceNotFoundException(BuildFlowException):
    """Raised when a resource is not found"""
    def __init__(self, resource: str, resource_id: int):
        message = f"{resource} with id {resource_id} not found"
        super().__init__(message, status_code=404)


class ValidationException(BuildFlowException):
    """Raised when validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class FileUploadException(BuildFlowException):
    """Raised when file upload fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class DatabaseException(BuildFlowException):
    """Raised when database operation fails"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=500)