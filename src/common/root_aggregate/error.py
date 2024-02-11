import traceback as tb


class Error(Exception):
    def __init__(self, message=None, origin: Exception = None, traceback=False):
        """
        Root exception type, base for all custom exception types.
        """

        # Adds traceback to log_message if True
        self._traceback = tb.format_exc()

        if origin:
            if message:
                self._error_message = f'{message}: {origin.__class__.__name__}: {str(origin)}'
            else:
                self._error_message = f'{origin.__class__.__name__}: {str(origin)}'
        else:
            self._error_message = message if message else ''

        self._error_message = (
            f'{self._error_message}\n{self._traceback}' if traceback else self._error_message
        )

        super().__init__(self._error_message)

    @property
    def traceback(self) -> str:
        """
        Property that contains the error traceback str.
        """
        return self._traceback


class NoRetryError(Exception):
    """
    Exception type stands for exceptions that should bypass retry mechanisms.
    """


class UnexpectedError(Error):
    """
    Exception type that stands for excpetions that were not deliberatly handled.
    """
