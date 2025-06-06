from fastapi import HTTPException, status


class AccountInactive(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail='Account is inactive')

class IncorrectLoginOrPassword(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect login or password')

class AccountNotVerify(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Account is not verify')