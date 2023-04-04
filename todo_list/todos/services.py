import uuid

from django.db import transaction

from todo_list.todos.models import Todo
from todo_list.users.models import User

from . import selectors


@transaction.atomic()
def create_new_todo(
    *,
    user: User,
    title: str,
    description: str = "",
) -> Todo:
    todo = Todo.objects.create(
        user=user,
        title=title,
        description=description if description else "",
    )

    todo.save()

    return todo


@transaction.atomic
def update_todo(
    *,
    id: uuid.UUID,
    user: User,
    title: str = "",
    description: str = "",
    order: int,
    completed: bool = None,
) -> Todo:
    todo = selectors.get_todo_item(id=id, user=user)

    todo.title = title if title else todo.title
    todo.description = description if description else todo.description
    todo.completed = completed if completed is not None else todo.completed
    todo.to(order)

    todo.save()

    return todo


@transaction.atomic
def delete_todo(
    *,
    id: uuid.UUID,
    user: User,
) -> None:
    todo = selectors.get_todo_item(id=id, user=user)
    todo.delete()

    return
