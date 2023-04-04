class ApplicationError(Exception):
    def __init__(self, message, code=None, extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra
        self.code = code
