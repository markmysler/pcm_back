from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.endpoints import auth, users, organizations, images

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.title = "PCM API"

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(organizations.router, prefix="/orgs", tags=["organizations"])
app.include_router(images.router, prefix="/images", tags=["images"])

@app.get("/")
def read_root():
    return {"Hello": "World"}