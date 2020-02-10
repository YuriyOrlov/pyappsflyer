class PyAFError(Exception):
    """Base app exception"""


class PyAFValidationError(PyAFError):
    """
    Error for wrong data passed.
    """


class PyAFCommunicationError(PyAFError):
    """
    Error for different communication errors
    """


class WebServerError(PyAFError):
    """Errors for web"""


class AuthenticationError(WebServerError):
    """Different auth errors"""


class PyAFProcessingError(PyAFError):
    """
    Error for different communication errors
    """

class PyAFUnknownError(PyAFError):
    """
    Error for different communication errors
    """