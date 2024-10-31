from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.endpoints import auth, users, organizations, images

Base.metadata.create_all(bind=engine)

app = FastAPI()
# Define allowed origins
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://pcm.peripeteia.com.ar",
    "https://api.peripeteia.com.ar",
    # add any other origins here
]

# Apply the CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows only specified origins
    allow_credentials=True,
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)
app.title = "PCM API"

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(organizations.router, prefix="/orgs", tags=["organizations"])
app.include_router(images.router, prefix="/images", tags=["images"])

@app.get("/")
def read_root():
    return {"Hello": "World"}