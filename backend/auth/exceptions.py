from fastapi import HTTPException, status
MISSING_JWT_TOKEN = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Отсутствует refresh токен!')

class AccountInactive(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail='Account is inactive')

class IncorrectLoginOrPassword(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect login or password')

class AccountNotVerify(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Account is not verify')

class TokenMissing(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token is missing')