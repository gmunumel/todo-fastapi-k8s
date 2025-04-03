from pydantic import BaseModel, ConfigDict


class TodoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

    def __repr__(self):
        return (
            f"TodoBase(title={self.title}, description={self.description}, "
            f"completed={self.completed})"
        )


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class TodoResponse(TodoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
