from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AuthenticationRequest(BaseModel):
    email: str
    password: str

class AuthenticationResponse(BaseModel):
    user_id: int
    token: str

@app.post('/authenticate', response_model=AuthenticationResponse)
def authenticate(request: AuthenticationRequest):
    email = request.email
    password = request.password

    # Реализуйте логику аутентификации и возврата токена или идентификатора сессии
    # ...

    # В случае ошибки аутентификации, возбуждаем исключение HTTPException
    raise HTTPException(status_code=401, detail='Authentication failed')

    # Верните токен или идентификатор сессии в виде объекта AuthenticationResponse
    return AuthenticationResponse(user_id=user_id, token=token)