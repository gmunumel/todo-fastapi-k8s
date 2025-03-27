from src.schemas.todo import TodoCreate, TodoUpdate
from src.crud.todo import create_todo, get_todo, get_todos, update_todo, delete_todo


TEST_DESCRIPTION = "Test Description"
TEST_TITLE = "Test Title"
NEW_TITLE = "New Title"
NEW_DESCRIPTION = "New Description"


def test_todo_create(db):
    todo_data = TodoCreate(
        title=TEST_TITLE, description=TEST_DESCRIPTION, completed=False
    )
    todo = create_todo(db, todo_data)
    assert todo.id is not None
    assert todo.title == TEST_TITLE
    assert todo.description == TEST_DESCRIPTION
    assert todo.completed is False


def test_todo_get_all(db):
    create_todo(
        db, TodoCreate(title="Todo 1", description="Description 1", completed=False)
    )
    create_todo(
        db, TodoCreate(title="Todo 2", description="Description 2", completed=True)
    )
    todos = get_todos(db)
    assert len(todos) == 2
    assert todos[0].title == "Todo 1"
    assert todos[1].title == "Todo 2"


def test_todo_get_one(db):
    todo = create_todo(
        db,
        TodoCreate(title=TEST_TITLE, description=TEST_DESCRIPTION, completed=False),
    )
    fetched_todo = get_todo(db, todo.id)
    assert fetched_todo is not None
    assert fetched_todo.id == todo.id
    assert fetched_todo.title == TEST_TITLE


def test_todo_update(db):
    todo = create_todo(
        db,
        TodoCreate(title="Old Title", description="Old Description", completed=False),
    )
    updated_data = TodoUpdate(
        title=NEW_TITLE, description=NEW_DESCRIPTION, completed=True
    )
    updated_todo = update_todo(db, todo.id, updated_data)
    assert updated_todo is not None
    assert updated_todo.title == NEW_TITLE
    assert updated_todo.description == NEW_DESCRIPTION
    assert updated_todo.completed is True


def test_todo_update_not_found(db):
    updated_data = TodoUpdate(
        title=NEW_TITLE, description=NEW_DESCRIPTION, completed=True
    )
    updated_todo = update_todo(db, -1, updated_data)
    assert updated_todo is None


def test_todo_delete(db):
    todo = create_todo(
        db,
        TodoCreate(title=TEST_TITLE, description=TEST_DESCRIPTION, completed=False),
    )
    deleted_todo = delete_todo(db, todo.id)
    assert deleted_todo is not None
    assert deleted_todo.id == todo.id

    fetched_todo = get_todo(db, todo.id)
    assert fetched_todo is None


def test_todo_delete_not_found(db):
    deleted_todo = delete_todo(db, -1)
    assert deleted_todo is None
