class AppError(Exception):
    """Safe application error whose message may be returned to the browser."""

    def __init__(self, code: str, message: str, status: int = 400):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status

    def as_dict(self) -> dict:
        return {"ok": False, "error": {"code": self.code, "message": self.message}}
