from django.urls import path

from . import api

app_name = "todos"
urlpatterns = [
    path(
        "",
        api.TodoListAPIView.as_view(),
        name="todo-list",
    ),
    path(
        "create/",
        api.TodoCreateAPIView.as_view(),
        name="create-todo-item",
    ),
]
