class APIException(Exception):
    """Occur when a task fail in the client, without any chance of continuing"""

class RequestAPIException(APIException):
    """Occur when there is an error in the request (e.g 404 or 400 or 500...)"""
    def __init__(self, *args, response, **kwargs):
        self.response = response
        self.message = self.printable_request() + "\r\n" + self.printable_reponse()
        super().__init__(self, self.message)

    def printable_request(self):
        """ Gives a fully printable version of the request """
        req = self.response.request
        msg = "-- Request : {} | {} -- \r\n".format(req.method, req.url)
        msg += "Headers: {} \r\n".format(str(req.headers))
        msg += "Body: {} \r\n\r\n".format(str(req.body))
        return msg

    def printable_reponse(self):
        """ Gives a fully printable version of the response """
        resp = self.response
        msg = "-- Reponse : {} -- \r\n".format(resp.status_code)
        msg += "Headers: {} \r\n".format(str(resp.headers))
        msg += "Body: {} \r\n\r\n".format(str(resp.content))
        return msg
