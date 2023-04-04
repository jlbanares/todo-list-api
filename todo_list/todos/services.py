from django.db import transaction

from todo_list.todos.models import Todo
from todo_list.users.models import User


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
        description=description,
    )

    todo.save()

    return todo
