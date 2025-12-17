from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found.", headers={'x-error-code': 'USER_NOT_FOUND'})

class EmailTakenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Email belongs to another user.", headers={'x-error-code': 'EMAIL_TAKEN'})