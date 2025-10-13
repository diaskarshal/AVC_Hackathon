class BuildFlowException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResourceNotFoundException(BuildFlowException):
    def __init__(self, resource: str, resource_id: int):
        message = f"{resource} with id {resource_id} not found"
        super().__init__(message, status_code=404)


class ValidationException(BuildFlowException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class FileUploadException(BuildFlowException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class DatabaseException(BuildFlowException):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=500)