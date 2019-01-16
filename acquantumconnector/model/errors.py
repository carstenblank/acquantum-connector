class AcQuantumRequestError(Exception):
    def __init__(self, message, status_code=None):
        # type: (str, int) -> None
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return 'AcRequestError: \'{}\''.format(self.message)

    def __repr__(self):
        return 'AcRequestError: \'{}\''.format(self.message)


class AcQuantumRequestForbiddenError(AcQuantumRequestError):
    def __init__(self, message='403 Forbidden'):
        # type: (str) -> None
        self.message = message

    def __str__(self):
        return '403 - AcRequestForbiddenError: \'{}\''.format(self.message)

    def __repr__(self):
        return '403 - AcRequestForbiddenError: \'{}\''.format(self.message)
