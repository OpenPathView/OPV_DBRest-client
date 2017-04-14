class APIException(Exception):
    """Occur when a task fail in the client, without any chance of continuing"""

class RequestAPIException(APIException):
    """Occur when there is an error in the request (e.g 404 or 400 or 500...)"""
    def __init__(self, *args, response, **kwargs):
        self.response = response
        super().__init__(self, *args, **kwargs)

