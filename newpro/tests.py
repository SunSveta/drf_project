from rest_framework.test import APITestCase
from rest_framework import status

from newpro.models import Course
from user.models import User

class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = User(email="admin@sky.pro")
        password = "UNloCKed"
        self.user.set_password(password)
        self.user.is_active = True
        self.user.is_superuser = True  # почему то у юзера не было доступа создавать уроки, пока не установила суперюзера...
        self.user.save()

        response = self.client.post("/user/api/token/", {"email": "admin@sky.pro", "password": "UNloCKed"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.client.force_authenticate(user=self.user) # Без принудительной аутентификации тоже не работало ничего(проверяла)


    def test_lesson_create(self):
        response = self.client.post("/newpro/lesson/create/", {
            "title": "second lesson 3",
            "description": "One more test3 lesson",
            "video_link": "https://www.youtube.com",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_detail(self):
        self.test_lesson_create()

        response = self.client.get('/newpro/lesson/retrieve/3/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {"id": 3, "title": "second lesson 3", "description": "One more test3 lesson", "video_link": "https://www.youtube.com"}
        self.assertEqual(response.json(), expected_data)

    def test_lesson_update(self):
        self.test_lesson_create()

        response = self.client.put('/newpro/lesson/update/4/', {
            "title": "new edit",
            "description": "One more test4 lesson",
            "video_link": "https://www.youtube.com"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {"id": 4, "title": "new edit", "description": "One more test4 lesson", "video_link": "https://www.youtube.com"}
        self.assertEqual(response.json(), expected_data)


    def test_lesson_delete(self):

        self.test_lesson_create()

        response = self.client.delete('/newpro/lesson/destroy/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = User(email="admin@sky.pro")
        password = "UNloCKed"
        self.user.set_password(password)
        self.user.is_superuser = True
        self.user.save()

        response = self.client.post("/user/api/token/", {"email": "admin@sky.pro", "password": "UNloCKed"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTНORIZATION=f"Bearer {self.access_token}")
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/newpro/create_course/", {"title":"Test course", "description": "test-test"})
        self.course = Course.objects.get(title="Test course")


    def test_subscription_create(self):
        response = self.client.post("/newpro/subscription/create/", {"course_id": {self.course.id}})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_subscription_update(self):
        self.test_subscription_create()

        response = self.client.put("/newpro/subscription/update/2/", {"course_id": {self.course.id}, "status": "inactive"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {"id": 2, "course_id": self.course.id, "status": "inactive"}
        self.assertEqual(response.json(), expected_data)


