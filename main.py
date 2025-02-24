import logging
import os
import dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from database import engine
import database
from routers import flashcards, auth, subjects, topics, sessions, feedbacks, users
from jose import jwt, JWTError


app = FastAPI()

dotenv.load_dotenv()

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Erro na rota {request.url.path}: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"message": "Ocorreu um erro interno no servidor"}
        )

@app.middleware("http")
async def middleware(request: Request, call_next):
    if request.url.path in ["/auth/signin", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    token = request.headers.get("Authorization")

    if token:
        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
            user_id = payload.get("id")
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

    response = await call_next(request)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'

    return response

database.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(flashcards.router)
app.include_router(subjects.router)
app.include_router(topics.router)
app.include_router(sessions.router)
app.include_router(feedbacks.router)
app.include_router(users.router)