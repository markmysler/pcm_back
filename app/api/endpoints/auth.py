from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import auth_service
from app.schemas.user import UserCreate
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.core.config import keycloak_openid
import app.messages.register as msg

router = APIRouter()

@router.post("/register", status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        result = auth_service.register_user(user, db)
        return JSONResponse(content=jsonable_encoder(result), status_code=201)

    except Exception as e:
        if str(e) == '409: b\'{"errorMessage":"User exists with same username"}\'':
            raise HTTPException(status_code=400, detail=msg.username_exists)
        elif str(e) == '409: b\'{"errorMessage":"User exists with same email"}\'':
            raise HTTPException(status_code=400, detail=msg.email_exists)
        else:
            raise HTTPException(status_code=400, detail=str(e))

@router.post("/token")
def get_token(email:str, password:str):
    token = keycloak_openid.token(email, password)
    return token
