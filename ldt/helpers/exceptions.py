# -*- coding: utf-8 -*-
""" LDT exceptions classes."""

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class LanguageError(Error):
    """Exception raised for non-existing languages.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
#        self.expression = expression
        self.message = message

class ResourceError(Error):
    """Exception raised for non-existing languages.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
#        self.expression = expression
        self.message = message

class DictError(Error):
    """Exception raised for non-existing relation types.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class AuthorizationError(Error):
    """Exception raised for non-existing relation types.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message