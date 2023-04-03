from collections.abc import Sequence
from typing import Any

from django.contrib.auth import get_user_model
from factory import Faker, LazyAttribute, post_generation
from factory.django import DjangoModelFactory


class MockUserFactory(DjangoModelFactory):
    """
    User Factory to seed local database for testing
    """

    username = LazyAttribute(lambda o: f"test-{o.mocked_username}")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = "testpassword123"
        self.set_password(password)

    class Params:
        mocked_username = Faker("user_name")

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class UserFactory(DjangoModelFactory):
    """
    User Factory for unit tests
    """

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
