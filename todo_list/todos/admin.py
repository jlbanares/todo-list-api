from django.contrib import admin

from todo_list.todos.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "title",
    ]
    search_fields = [
        "id",
        "title",
    ]
    ordering = ["-updated_at"]
    autocomplete_fields = ["user"]
