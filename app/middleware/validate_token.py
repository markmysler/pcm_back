from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from app.core.config import keycloak_openid

class ValidateToken(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(ValidateToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if credentials:
            token_info = keycloak_openid.introspect(credentials.credentials)
            if not token_info or token_info['active'] is False:
                raise HTTPException(status_code=401, detail="Invalid token")
            return token_info
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")