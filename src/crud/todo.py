from sqlalchemy.orm import Session

from src.models.todo import Todo
from src.schemas.todo import TodoCreate, TodoUpdate
from src.log import logger


def get_todos(db: Session):
    logger.info("Fetching all todos")
    return db.query(Todo).all()


def get_todo(db: Session, todo_id: int):
    logger.info("Fetching one todo with id: %s", todo_id)
    return db.query(Todo).filter(Todo.id == todo_id).first()


def create_todo(db: Session, todo: TodoCreate):
    logger.info("Creating a new todo with info: %s", todo)
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: TodoUpdate):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        logger.info("Updating todo with id: %s, info: %s", todo_id, todo)
        for key, value in todo.model_dump(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        logger.info("Deleting todo with id: %s", todo_id)
        db.delete(db_todo)
        db.commit()
    return db_todo
