from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import auth_service
from app.schemas.user import UserCreate, TokenRequest
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.core.config import keycloak_openid, keycloak_admin
import app.messages.register as msg
from pydantic import EmailStr

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
def get_token(data: TokenRequest):
    try:
        token = keycloak_openid.token(data.email, data.password)
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/reset-password")
def reset_password(email:str):
    # Trigger a password reset email
    try:
    # Get the user ID for the given email or username
        user_id = keycloak_admin.get_user_id(email)
    
    # Send a password reset email
        keycloak_admin.send_update_account(user_id, ["UPDATE_PASSWORD"])
        return JSONResponse(content="Password reset email sent successfully.", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to send password reset email: {str(e)}")