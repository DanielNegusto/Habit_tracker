from celery import shared_task

from .services import send_reminder
from .models import Habit
import logging

logger = logging.getLogger(__name__)


@shared_task
def schedule_daily_reminders():
    habits = Habit.objects.filter(is_pleasant=False).select_related("linked_habit")

    user_habits = {}
    for habit in habits:
        user_habits.setdefault(habit.user.id, []).append(habit)

    for user_id, user_habits_list in user_habits.items():
        habit_messages = []
        for habit in user_habits_list:
            if habit.reward:
                reward = habit.reward
            elif habit.linked_habit:
                reward = (
                    habit.linked_habit.action
                )
            else:
                reward = "Нет награды"

            habit_messages.append(
                f'Сегодня нужно "{habit.action}" в {habit.time.strftime("%H:%M")} в {habit.place}. Награда: {reward}'
            )

        if habit_messages:
            message = "Сегодня у вас следующие привычки:\n" + "\n".join(habit_messages)
            send_reminder(user_id, message)
        else:
            logger.info(
                f"У пользователя с id {user_id} нет привычек на сегодня или все привычки приятные."
            )
