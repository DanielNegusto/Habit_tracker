from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Habit


class HabitViewSetTests(APITestCase):

    def setUp(self):
        # Создаем пользователя для тестов
        self.user = User.objects.create_user(email='test@test.com', password='password')

        # Создаем привычку для тестирования
        self.habit = Habit.objects.create(action='Test Habit', time='15:00', place='Test Place', estimated_time='120',
                                          user=self.user, is_public=False, reward="reward", is_pleasant=False)

    def test_create_habit(self):
        """Тестирование создания привычки"""
        self.client.force_authenticate(user=self.user)
        url = "/api/habits/"
        data = {'action': 'New Habit', 'time': '11:00', 'place': 'Test Place', 'estimated_time': '120',
                'is_public': False, 'reward': "reward", 'is_pleasant': False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_list_habits(self):
        """Тестирование получения списка привычек"""
        self.client.force_authenticate(user=self.user)
        url = "/api/habits/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.count(), 1)

    def test_get_public_habits(self):
        """Тестирование получения публичных привычек"""
        self.client.force_authenticate(user=self.user)
        url = "/api/habits/public/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.count(), 1)

    def test_get_pleasant_habits(self):
        """Тестирование получения приятных привычек"""
        self.client.force_authenticate(user=self.user)
        url = "/api/habits/pleasant/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
