from rest_framework.exceptions import APIException


class BaseAPIException(APIException):

    status_code = None
    detail = None

    def __init__(self, status_code, message):
        self.__class__.status_code = status_code
        self.__class__.detail = message


class CouldNotCreateObject(BaseAPIException):
    """ Raises if object can not be created properly. """


class InvalidParameter(BaseAPIException):
    """ Raises if parameter is invalid. """


__all__ = [
    'CouldNotCreateObject',
    'InvalidParameter',
]
