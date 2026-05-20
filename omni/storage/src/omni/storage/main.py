"""

Links:
https://camillovisini.com/article/abstracting-FastAPI-services/
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from omni.storage.src.omni.storage.routers import users_route
from omni.storage.src.omni.storage.repositories.models.user_sqlalchemy_model import Base
from omni.storage.src.omni.storage.repositories.implementations.sessions.sqlalchemy_session import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_route.router)


@app.on_event("startup")
def tables_creation():
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """
    Message for root GET.
    """
    return {"status": 200, "message": "This API is alive."}
