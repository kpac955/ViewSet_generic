from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class MaterialsTestCase(APITestCase):

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.user = User.objects.create(email="test@test.com")
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title="Django", description="Backend development", owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title="DRF Tests",
            course=self.course,
            owner=self.user,
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )

    def test_lesson_retrieve(self):
        """Тест получения одного урока."""
        response = self.client.get(f"/lesson/{self.lesson.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "DRF Tests")

    def test_lesson_create_valid(self):
        """Тест создания урока с правильной ссылкой на YouTube."""
        data = {
            "title": "New Lesson",
            "description": "Some description",  # Добавь описание, если оно обязательно в модели
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
        response = self.client.post("/lesson/create/", data=data)

        if response.status_code != status.HTTP_201_CREATED:
            print(f"\nОшибка валидации: {response.json()}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create_invalid_link(self):
        """Тест валидатора: запрет ссылок не на YouTube."""
        data = {
            "title": "Invalid Lesson",
            "course": self.course.id,
            "video_url": "https://rutube.ru/video/123",
        }
        response = self.client.post("/lesson/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Допускаются ссылки только на youtube.com", response.data["video_url"][0]
        )

    def test_subscription_toggle(self):
        """Тест работы эндпоинта подписки (создание/удаление)."""
        data = {"course": self.course.id}

        response = self.client.post("/subscribe/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.post("/subscribe/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_lesson_list_pagination(self):
        """Тест наличия пагинации в списке уроков."""
        response = self.client.get("/lesson/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
