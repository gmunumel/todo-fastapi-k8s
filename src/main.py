from fastapi import FastAPI

from src.routers import todo
from src.database import Base, engine
from src.log import logger

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(todo.router, prefix="/api/v1/todos", tags=["Todos"])

logger.info("FastAPI application has started.")
