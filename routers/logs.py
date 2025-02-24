from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from models.requests_model import ErrorLog


router = APIRouter(
    prefix='/logs',
    tags=['logs']
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def receive_log(log: ErrorLog):
    try:
        print("Novo log de erro recebido:")
        print(log.model_dump())
        
        return JSONResponse(content={"message": "Log recebido com sucesso!"}, status_code=status.HTTP_201_CREATED)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
