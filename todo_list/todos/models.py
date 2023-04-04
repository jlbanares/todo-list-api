import uuid

from django.db import models
from django.utils import timezone
from ordered_model.models import OrderedModel


class Todo(OrderedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    # Subset Ordering - https://github.com/django-ordered-model/django-ordered-model#subset-ordering
    # Allow users to order their own todos regardless of how other users choose their order
    order_with_respect_to = "user"

    def __str__(self) -> str:
        return self.title
