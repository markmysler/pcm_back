from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import auth_service
from app.middleware.validate_token import ValidateToken
from app.schemas.user import UserOut
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/me", response_model=UserOut, status_code=200)
async def get_user_info(
    token_info: str = Depends(ValidateToken()),
    db: Session = Depends(get_db)
):
    try:
        user_info = auth_service.get_user_info(token_info, db)
        return JSONResponse(content=jsonable_encoder(user_info), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
