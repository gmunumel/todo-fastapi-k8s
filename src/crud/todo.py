from sqlalchemy.orm import Session

from src.models.todo import Todo
from src.schemas.todo import TodoCreate, TodoUpdate


def get_todos(db: Session):
    return db.query(Todo).all()


def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: TodoUpdate):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        for key, value in todo.model_dump(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
