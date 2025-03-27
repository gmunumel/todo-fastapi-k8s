from fastapi import FastAPI

from src.routers import todo
from src.database import Base, engine

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(todo.router, prefix="/api/v1/todos", tags=["Todos"])
