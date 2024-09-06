from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.config import keycloak_admin
import app.messages.register as msg
from app.core.config import keycloak_openid


def get_user_info(token_info, db: Session):
    return db.query(User).filter_by(id=token_info['sub']).first()

def register_user(user: UserCreate, db: Session):
    # Créer l'utilisateur dans Keycloak
    new_kc_user = {
        "username": user.username,
        "email": user.email,
        "enabled": True,
        "firstName": user.name,
        "lastName": user.surname,
        "credentials": [{
            "type": "password",
            "value": user.password,
            "temporary": False
        }],
    }

    kc_id = keycloak_admin.create_user(new_kc_user, exist_ok=False)
    new_db_user = User(
        id=kc_id,
        name=user.name,
        surname=user.surname,
        username=user.username,
        email=user.email,
        is_verified=False
    )
    db.add(new_db_user)
    db.commit()

    # Générer le token d'accès pour l'utilisateur
    token = keycloak_openid.token(user.username, user.password)

    return {
        "message": msg.registration_success,
        "access_token": token['access_token'],
        "token_type": token['token_type']
    }
