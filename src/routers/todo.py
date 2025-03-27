from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from src.crud.todo import get_todos, get_todo, create_todo, update_todo, delete_todo

router = APIRouter()

TODO_NOT_FOUND = "Todo not found"


@router.get("/", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    return get_todos(db)


@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo


@router.post("/", response_model=TodoResponse)
def create_new_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db, todo)


@router.put("/{todo_id}", response_model=TodoResponse)
def update_existing_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    updated_todo = update_todo(db, todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return updated_todo


@router.delete("/{todo_id}", response_model=TodoResponse)
def delete_existing_todo(todo_id: int, db: Session = Depends(get_db)):
    deleted_todo = delete_todo(db, todo_id)
    if not deleted_todo:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return deleted_todo
