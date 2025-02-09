from django.core.exceptions import ValidationError


def validate_habit_fields(habit):
    if habit.linked_habit and habit.reward:
        raise ValidationError(
            "Укажите только одно из полей: вознаграждение или связанная привычка."
        )

    if habit.estimated_time > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")

    if habit.frequency < 1 or habit.frequency > 7:
        raise ValidationError(
            "Периодичность выполнения привычки должна быть от 1 до 7 дней."
        )

    if habit.is_pleasant and (habit.reward or habit.linked_habit):
        raise ValidationError(
            "Приятная привычка не может иметь вознаграждение или связанную привычку."
        )
