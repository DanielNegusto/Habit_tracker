from rest_framework import serializers
from .models import Habit
from .validators import validate_habit_fields


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit.

    Этот сериализатор преобразует экземпляры модели Habit в формат JSON
    и обратно, а также предоставляет дополнительные поля и валидацию.

    Атрибуты:
        title (str): Название привычки, основанное на ее типе (приятная или полезная).
        linked_habit (PrimaryKeyRelatedField): Связанная привычка, которая является приятной.
        linked_habit_action (str): Действие связанной привычки.
        owner (str): Электронная почта пользователя, которому принадлежит привычка.
    """

    title = serializers.SerializerMethodField()
    linked_habit = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.filter(is_pleasant=True), required=False
    )
    linked_habit_action = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = [
            "title",
            "id",
            "action",
            "place",
            "time",
            "is_pleasant",
            "reward",
            "frequency",
            "estimated_time",
            "is_public",
            "owner",
            "linked_habit",
            "linked_habit_action",
        ]

    def get_linked_habit_action(self, obj):
        """
        Получает действие связанной привычки.

        Аргументы:
            obj (Habit): Экземпляр привычки.

        Возвращает:
            str: Действие связанной привычки, если она существует, иначе None.
        """
        if obj.linked_habit:
            return obj.linked_habit.action
        return None

    def get_owner(self, obj):
        """
        Получает электронную почту владельца привычки.

        Аргументы:
            obj (Habit): Экземпляр привычки.

        Возвращает:
            str: Электронная почта пользователя, которому принадлежит привычка.
        """
        return obj.user.email

    def get_title(self, obj):
        """
        Получает название привычки.

        Аргументы:
            obj (Habit): Экземпляр привычки.

        Возвращает:
            str: Название привычки, основанное на ее типе (приятная или полезная).
        """
        return "Полезная привычка" if not obj.is_pleasant else "Приятная привычка"

    def validate(self, attrs):
        """
        Валидация полей привычки.

        Аргументы:
            attrs (dict): Словарь атрибутов привычки.

        Возвращает:
            dict: Проверенные и валидированные атрибуты привычки.

        Исключения:
            Raises ValidationError, если валидация не проходит.
        """
        habit = Habit(**attrs)
        validate_habit_fields(habit)
        return attrs
