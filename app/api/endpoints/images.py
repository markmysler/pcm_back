import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from app.models.user import User
from app.services import image_service
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.validate_token import ValidateToken
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/", status_code=201)
async def upload_image(
    file: UploadFile,
    token_info: str = Depends(ValidateToken()),
    db: Session = Depends(get_db)
):
    try:
        # existe el usuario?
        user = db.query(User).filter_by(id=token_info['sub']).first()
        if not user or user is None: raise HTTPException(status_code=404, detail="User not found")
        
        # subir img
        url = await image_service.upload_image(file, "static/images/", uuid.uuid4().hex)
        
        # devolver url
        return JSONResponse(content=jsonable_encoder(url), status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
