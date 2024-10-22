import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from app.models.user import User
from app.enums.roles import UserRole
from app.models.organization import Organization
from app.services import image_service
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.validate_token import ValidateToken
from app.schemas.organization import OrgOut, OrgCreate
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/", response_model=OrgOut, status_code=201)
async def create_organization(
    org: OrgCreate,
    token_info: str = Depends(ValidateToken()),
    db: Session = Depends(get_db)
):
    try:
        # existe el usuario?
        user = db.query(User).filter_by(id=token_info['sub']).first()
        if not user or user is None: raise HTTPException(status_code=404, detail="User not found")
        # revisar que sea super admin
        if user.role != UserRole.SUPER_ADMIN: raise HTTPException(status_code=404, detail="Not allowed")
        # crear organizacion con args
        new_org = Organization(
            name=org.name,
            manager=org.manager
        )
        db.add(new_org)
        db.commit()
        db.refresh(new_org)
        # devolver objeto nueva org
        return JSONResponse(content=jsonable_encoder(new_org), status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
   
@router.post("/logo/{org_id}", response_model=OrgOut, status_code=200)
async def update_organization_logo(
    org_id:int,
    file: UploadFile,
    token_info: str = Depends(ValidateToken()),
    db: Session = Depends(get_db)
):
    try:
        
        # existe el usuario?
        user = db.query(User).filter_by(id=token_info['sub']).first()
        if not user or user is None: raise HTTPException(status_code=404, detail="User not found")
        # existe la org?
        org = db.query(Organization).filter_by(id=org_id).first()
        if not org or org is None: raise HTTPException(status_code=404, detail="Organization not found")
        # revisar que sea super admin, periadmin o manager/admin de org
        if user.role == UserRole.USER or (user.role in [UserRole.ORG_ADMIN, UserRole.MANAGER] and user.organization != org_id):
            raise HTTPException(status_code=404, detail="Not allowed")
        # subir img
        new_url = await image_service.upload_image(file, "static/logos/", uuid.uuid4().hex)
        # org tenia img? borrar
        if org.logo is not None:
            await image_service.delete_image_by_url(org.logo)
        # actualizar logo
        org.logo = new_url
        db.commit()
        db.refresh(org)
        # devolver url
        return JSONResponse(content=jsonable_encoder(org), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 
@router.put("/{org_id}", response_model=OrgOut, status_code=200)
async def change_organization_name(
    org_id:int,
    name: str,
    token_info: str = Depends(ValidateToken()),
    db: Session = Depends(get_db)
):
    try:
        
        # existe el usuario?
        user = db.query(User).filter_by(id=token_info['sub']).first()
        if not user or user is None: raise HTTPException(status_code=404, detail="User not found")
        # existe la org?
        org = db.query(Organization).filter_by(id=org_id).first()
        if not org or org is None: raise HTTPException(status_code=404, detail="Organization not found")
        # revisar que sea super admin, periadmin o manager/admin de org
        if user.role == UserRole.USER or (user.role in [UserRole.ORG_ADMIN, UserRole.MANAGER] and user.organization != org_id): raise HTTPException(status_code=404, detail="Not allowed")
        # actualizar nombre args
        org.name = name
        db.commit()
        db.refresh(org)
        # devolver objeto org
        return JSONResponse(content=jsonable_encoder(org), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{org_id}", response_model=OrgOut, status_code=200)
async def delete_organization(
    org_id:int,
    token_info: str = Depends(ValidateToken()),
    db: Session = Depends(get_db)
):
    try:
        
        # existe el usuario?
        user = db.query(User).filter_by(id=token_info['sub']).first()
        if not user or user is None: raise HTTPException(status_code=404, detail="User not found")
        # existe la org?
        org = db.query(Organization).filter_by(id=org_id).first()
        if not org or org is None: raise HTTPException(status_code=404, detail="Organization not found")
        # revisar que sea super admin
        if user.role != UserRole.SUPER_ADMIN: raise HTTPException(status_code=404, detail="Not allowed")
        # actualizar nombre args
        db.delete(org)
        db.commit()
        # devolver objeto org
        return JSONResponse(content=jsonable_encoder("Organization deleted"), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
