from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from todo_list.common.api.mixins import APIErrorsMixin
from todo_list.todos.models import Todo
from todo_list.utils.pagination import LimitOffsetPagination, get_paginated_response

from . import selectors, services


class TodoDetailAPIView(APIErrorsMixin, APIView):
    class TodoItemDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            exclude = ("user",)

    def get(self, request, id):
        """
        Return a specific todo of a user
        """

        todo_item = selectors.get_todo_item(
            id=id,
            user=request.user,
        )

        data = self.TodoItemDetailSerializer(todo_item).data
        return Response(data, status=status.HTTP_200_OK)


class TodoListAPIView(APIErrorsMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 20
        max_limit = 100

    pagination_class = Pagination

    class TodoListFilterSerializer(serializers.Serializer):
        completed = serializers.BooleanField(
            required=False,
            allow_null=True,
            default=None,
        )

    class TodoListResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            exclude = ("user",)

    @extend_schema(
        responses={200: TodoListResponseSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                "completed",
                OpenApiTypes.BOOL,
                OpenApiParameter.QUERY,
                description="Filter todos to completed or non-completed only. Leave blank if both.",
                required=False,
            )
        ],
    )
    def get(self, request):
        """
        Return all todos of a user ordered according to the ranking of the user

        Returns both completed and non-completed Todos by default
        """

        filters = self.TodoListFilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)

        todo_list = selectors.get_todo_list(
            user=request.user,
            filters=filters.validated_data,
        )

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.TodoListResponseSerializer,
            queryset=todo_list,
            request=request,
            view=self,
        )


class TodoCreateAPIView(APIErrorsMixin, APIView):
    class TodoCreateRequestSerializer(serializers.Serializer):
        title = serializers.CharField()
        detail = serializers.CharField(
            required=False,
            default="",
            allow_blank=True,
        )

    class TodoCreateResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            exclude = ("user",)

    @extend_schema(
        request=TodoCreateRequestSerializer,
        responses={201: TodoCreateResponseSerializer},
    )
    def post(self, request):
        """
        Create new a new todo item
        """
        body = self.TodoCreateRequestSerializer(data=request.data)
        body.is_valid(raise_exception=True)
        params = body.validated_data

        todo = services.create_new_todo(
            user=request.user,
            title=params["title"],
            description=params.get("description"),
        )

        data = self.TodoCreateResponseSerializer(todo).data
        return Response(data, status=status.HTTP_201_CREATED)


class TodoUpdateAPIView(APIErrorsMixin, APIView):
    class TodoUpdateRequestSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        detail = serializers.CharField(required=False)
        completed = serializers.BooleanField(required=False)
        order = serializers.IntegerField(min_value=0)

    class TodoUpdateResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            exclude = ("user",)

    @extend_schema(
        request=TodoUpdateRequestSerializer,
        responses={200: TodoUpdateResponseSerializer},
    )
    def put(self, request, id):
        """
        Update a todo item's details

        This will only proceed if the user owns the todo ID provided.

        Only the order field is required on the request body.
        If updating only the order (rank) of the TODO item, then only provide the order.
        """
        body = self.TodoUpdateRequestSerializer(data=request.data)
        body.is_valid(raise_exception=True)
        params = body.validated_data

        updated_todo = services.update_todo(
            id=id,
            user=request.user,
            title=params.get("title"),
            description=params.get("description"),
            completed=params.get("completed"),
            order=params["order"],
        )

        data = self.TodoUpdateResponseSerializer(updated_todo).data
        return Response(data, status=status.HTTP_200_OK)


class TodoDeleteAPIView(APIErrorsMixin, APIView):
    def delete(self, request, id):
        """
        Delete a specific todo item

        This will only proceed if the user owns the todo ID provided.
        """
        services.delete_todo(id=id, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
