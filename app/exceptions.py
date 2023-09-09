from fastapi import HTTPException, status


class TaskException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(TaskException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class CannotAddDataToDatabase(TaskException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось добавить запись"