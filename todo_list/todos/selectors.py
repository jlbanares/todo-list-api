from django.db.models import QuerySet

from todo_list.todos.models import Todo
from todo_list.users.models import User


def get_todo_list(
    *,
    user: User,
    filters: dict = None,
) -> QuerySet[Todo]:
    """
    Return all the todos associated with a user
    """

    filters = filters or {}

    if filters.get("completed") is None:
        del filters["completed"]

    return Todo.objects.filter(user=user, **filters).order_by("order")
