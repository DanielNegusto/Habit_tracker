from django.db import models
from users.models import User


class Habit(models.Model):
    """
    Модель, представляющая привычку пользователя.

    Атрибуты:
        user (ForeignKey): Пользователь, которому принадлежит привычка.
        action (str): Действие, которое представляет привычка.
        place (str): Место, где будет осуществляться действие.
        time (TimeField): Время, когда привычка будет выполняться.
        is_pleasant (bool): Указывает, является ли привычка приятной (по умолчанию False).
        linked_habit (ForeignKey): Связанная привычка, которая является приятной.
        reward (str): Награда за выполнение привычки (может быть пустой).
        frequency (PositiveIntegerField): Частота выполнения привычки (по умолчанию 1).
        estimated_time (PositiveIntegerField): Оценочное время выполнения привычки.
        is_public (bool): Указывает, является ли привычка публичной (по умолчанию False).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_pleasant": True},
        related_name="reward_habit",
    )
    reward = models.CharField(max_length=255, null=True, blank=True)
    frequency = models.PositiveIntegerField(default=1)
    estimated_time = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)

    def __str__(self):
        """
        Возвращает строковое представление привычки.

        Возвращает:
            str: Описание привычки, включая ее тип (приятная или полезная),
                 действие, место и время.
        """
        return (
            f"{'Приятная' if self.is_pleasant else 'Полезная'} привычка\n"
            f"Я буду {self.action} в {self.place} в {self.time}"
        )
