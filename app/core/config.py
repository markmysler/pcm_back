import os
from keycloak import KeycloakOpenID, KeycloakAdmin, KeycloakOpenIDConnection
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    pgadmin_default_email: str
    pgadmin_default_password: str
    secret_key: str
    api_db_name: str
    api_db_user: str
    api_db_password: str
    base_url:str
    
    # SMTP Settings
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

load_dotenv(dotenv_path=".env.keycloak")

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("KC_URL","http://keycloak:8080"),
    client_id=os.getenv("KC_CLIENT_ID","pcm-api-client"),
    realm_name=os.getenv("KC_REALM","pcm-api"),
    client_secret_key=os.getenv("KC_CLIENT_SECRET","my_precious")
)

keycloak_connection = KeycloakOpenIDConnection(
    server_url=os.getenv("KC_URL", "http://keycloak:8080"),
    username=os.getenv("KEYCLOAK_REALM_ADMIN", "pcm-admin"),
    password=os.getenv("KEYCLOAK_REALM_ADMIN_PASSWORD","admin_password"),
    realm_name=os.getenv("KC_REALM", "pcm-api"),
    verify=True
)
keycloak_admin = KeycloakAdmin(connection=keycloak_connection)

MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB
TARGET_FILE_RES = (512, 512) # px