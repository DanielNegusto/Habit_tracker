from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Habit
from .serializers import HabitSerializer
from .paginators import CustomPagination


class HabitViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления привычками.

    Этот вьюсет предоставляет CRUD операции для модели Habit,
    включая возможность получения публичных и приятных привычек.

    Атрибуты:
        serializer_class (Serializer): Сериализатор, используемый для преобразования данных.
        permission_classes (list): Список разрешений для доступа к API.
        pagination_class (Pagination): Класс пагинации для управления количеством объектов на странице.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """
        Сохраняет новый экземпляр привычки с привязкой к текущему пользователю.

        Аргументы:
            serializer (HabitSerializer): Сериализатор для создания привычки.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Получает queryset привычек, принадлежащих текущему пользователю.

        Возвращает:
            QuerySet: Привычки, связанные с текущим пользователем.
        """
        return Habit.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def public(self, request):
        """
        Получает публичные привычки.

        Этот метод доступен для всех пользователей, включая неавторизованных.

        Аргументы:
            request (Request): HTTP запрос.

        Возвращает:
            Response: Ответ с данными публичных привычек, возможно с пагинацией.
        """
        public_habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def pleasant(self, request):
        """
        Получает приятные привычки текущего пользователя.

        Этот метод доступен только для авторизованных пользователей.

        Аргументы:
            request (Request): HTTP запрос.

        Возвращает:
            Response: Ответ с данными приятных привычек, возможно с пагинацией.
        """
        pleasant_habits = Habit.objects.filter(user=self.request.user, is_pleasant=True)
        page = self.paginate_queryset(pleasant_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(pleasant_habits, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Получает список полезных привычек текущего пользователя.

        Аргументы:
            request (Request): HTTP запрос.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            Response: Ответ с данными неприятных привычек, возможно с пагинацией.
        """
        # Получаем только неприятные привычки
        queryset = self.get_queryset().filter(is_pleasant=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
