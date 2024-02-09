from fastapi import FastAPI
from database import engine
import database
from routers import flashcards, auth, subjects, topics


app = FastAPI()

database.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(flashcards.router)
app.include_router(subjects.router)
app.include_router(topics.router)