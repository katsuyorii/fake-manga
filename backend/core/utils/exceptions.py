from fastapi import HTTPException, status


class EmailAlreadyRegistered(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail='Email is already registered')