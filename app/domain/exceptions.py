class NotFoundError(Exception):
    """指定されたリソースが存在しない場合に送出する。"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
