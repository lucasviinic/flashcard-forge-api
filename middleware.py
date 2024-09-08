import os

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt, JWTError


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

app = FastAPI()

@app.middleware("http")
async def middleware(request: Request, call_next):
    if request.url.path in ["/auth/signin", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    token = request.headers.get("Authorization")
    if token:
        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except JWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token inválido ou expirado."}
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token de autenticação não fornecido."}
        )

    return await call_next(request)