from django.urls import path

from . import api

app_name = "todos"
urlpatterns = [
    path(
        "",
        api.TodoListAPIView.as_view(),
        name="get-todo-list",
    ),
    path(
        "create/",
        api.TodoCreateAPIView.as_view(),
        name="create-todo-item",
    ),
    path(
        "<str:id>/",
        api.TodoDetailAPIView.as_view(),
        name="get-todo-item",
    ),
    path(
        "<str:id>/update/",
        api.TodoUpdateAPIView.as_view(),
        name="update-todo-item",
    ),
    path(
        "<str:id>/delete/",
        api.TodoDeleteAPIView.as_view(),
        name="delete-todo-item",
    ),
]
