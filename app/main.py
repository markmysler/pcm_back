from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.endpoints import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.title = "PCM API"

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"Hello": "World"}