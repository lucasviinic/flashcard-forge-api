from typing import Annotated
from starlette import status

from utils import pdf_to_text
from usecases.flashcards import generate_flashcards_usecase

from fastapi import APIRouter, HTTPException, UploadFile


router = APIRouter()

@router.post("/flashcards", status_code=status.HTTP_201_CREATED)
async def generate_flashcards(file: UploadFile, quantity: int = 5):
    try:
        text_content = pdf_to_text(pdf=file.file)
        flashcards_list = generate_flashcards_usecase(text_content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro durante a conversão do PDF: {str(e)}")

    return {"flashcards": flashcards_list}