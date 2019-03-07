"""
	Base Error handler
    NOT INTENDED TO USE DIRECTLY
"""
class BaseError(Exception):
    """ base error class """
    def __init__(self, error, code, message, details):
        super().__init__(error, code, message, details)
        self.error = error
        self.code = code
        self.message = message
        self.details = details

    def to_dict(self):
        """
	        Call this in the the error handler to serialize the
	        error for the json-encoded http response body.
        """
        error_response = {
            "error"   : self.error,
            "message" : self.message,
        }
        if self.details is not None:
            error_response["details"] = self.details
        return error_response

class BadRequest(BaseError):
    """ base http error class for any bad request"""
    def __init__(self, error=None, message=None, details=None):
        super(BaseError, self).__init__(message, details)
        self.code = 400

        if error is None:
            self.error = "BAD_REQUEST"
        else:
            self. error = error

        self.message = message
        self.details = details

class RequestNotFound(BaseError):
    """ base http error class for any resource not found"""
    def __init__(self, error=None, message=None, details=None):
        super(BaseError, self).__init__(message, details)
        self.code = 404

        if error is None:
            self.error = "REQUEST_NOT_FOUND"
        else:
            self. error = error

        self.message = message
        self.details = details

class UnprocessableEntity(BaseError):
    """ base http error class for any resource not found"""
    def __init__(self, error=None, message=None, details=None):
        super(BaseError, self).__init__(message, details)
        self.code = 422

        if error is None:
            self.error = "UNPROCESSABLE_ENTITY"
        else:
            self. error = error

        self.message = message
        self.details = details

class Unauthorized(BaseError):
    """ base http error class for unauthorized access"""
    def __init__(self, message=None, details=None):
        super(BaseError, self).__init__(message, details)
        self.code = 401
        self.error = "UNAUTHORIZED"
        self.message = message
        self.details = details
