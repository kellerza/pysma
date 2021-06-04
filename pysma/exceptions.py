"""Exceptions for the pysma library."""


class SmaException(Exception):
    """Base exception of the pysma library."""


class SmaAuthenticationException(SmaException):
    """An attempt to authenticate failed."""


class SmaReadException(SmaException):
    """Reading the data did not return an expected result."""


class SmaConnectionException(SmaException):
    """An error occurred in the connection with the device."""
