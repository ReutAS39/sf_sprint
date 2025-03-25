import json

from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pereval.models import PerevalAdded, PerevaladdedImages, Images, Users, Coords, Level
from pereval.serializers import PerevalSerializer

client = Client()


class CreateNewPerevalTest(APITestCase):
    """ Test module for inserting a new pereval """

    def setUp(self):
        self.valid_payload = {
            "user": {
                "email": "test@example.com",
                "phone": "+79226120668",
                "fam": "Пупкин",
                "name": "Васиилий",
                "otc": "Иванович"
            },
            "coords": {
                "latitude": 43.17257,
                "longitude": 42.80231,
                "height": 3710
            },
            "level": {
                "winter": "2А",
                "summer": "1Б",
                "autumn": "1Б",
                "spring": "1Б"
            },
            "images": [
                {
                    "data": "http://127.0.0.1:8000/photos/2023/04/11/19._%D0%A1%D0%B0%D0%BC%D0%BE%D0%.jpg",
                    "title": "Вид с вершины"
                }
            ],
            "beauty_title": "пер.",
            "title": "Гарваш",
            "other_titles": "",
            "connect": ""
        }

        self.invalid_payload = {
            'user': {
                'name': 12,
                'fam': '',
                'otc': 'Test Otc',
                'email': '',
                'phone': '+735454521452528'
            },
            'coords': {
                'latitude': 123,
                'longitude': 678.9,
                'height': '777',
            },
            'level': {
                'winter': '1А',
                'summer': 'н/к',
                'autumn': 'н/к',
                'spring': 'Tн/к'
            },
            'images': [
                {
                    'title': 'Test Image',
                    'img': 'test.jpg'
                }
            ]
        }

    def test_create_valid_pereval(self):
        response = client.post(
            reverse('submitData-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_pereval(self):
        response = client.post(
            reverse('submitData-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetPatchSinglePerevalTest(APITestCase):
    """ Test module for GET and PATCH single pereval API """
    def setUp(self):
        self.level = Level.objects.create(winter='1А', summer='1А', autumn='1Б', spring='1Б')
        self.coords = Coords.objects.create(latitude=33.3, longitude=55.5, height=777)
        self.user = Users.objects.create(email='test@test.ru', phone='+79521542323', name='Тест', fam='Тес', otc='Тест')
        self.image = Images.objects.create(title='Тест заголовок', data='https://test.ru/uploads/2020/08/test-36.jpg')
        self.pereval = PerevalAdded.objects.create(user=self.user, coords=self.coords, level=self.level)
        self.perevalimages = PerevaladdedImages.objects.create(images=self.image, perevaladded=self.pereval)

        self.valid_payload = {
            "user": {
                "email": "test@example.com",
                "phone": "+79226120668",
                "fam": "Пупкин",
                "name": "Васиилий",
                "otc": "Иванович"
            },
            "coords": {
                "latitude": 43.17257,
                "longitude": 42.80231,
                "height": 3710
            },
            "level": {
                "winter": "2А",
                "summer": "1Б",
                "autumn": "1Б",
                "spring": "1Б"
            },
            "images": [
                {
                    "data": "http://127.0.0.1:8000/photos/2023/04/11/19._%D0%A1%D0%B0%D0%BC%D0%BE%D0%%D1%8B.jpg",
                    "title": "Вид с вершины"
                }
            ],
            "beauty_title": "пер.",
            "title": "Гарвашииии",
            "other_titles": "",
            "connect": ""
        }

        self.invalid_payload = {
            'user': {
                'name': 12,
                'fam': 'Test Fam',
                'otc': 'Test Otc',
                'email': '',
                'phone': '+73521452528'
            },
            'coords': {
                'latitude': 123,
                'longitude': 678.9,
                'height': 777,
            },
            'level': {
                'winter': '1А',
                'summer': 'н/к',
                'autumn': 'н/к',
                'spring': 'Tн/к'
            },
            'images': [
                {
                    'title': 'Test Image',
                    'img': 'test.jpg'
                }
            ],
            "beauty_title": "пер.",
            "title": "Гарваш",
            "other_titles": "",
            "connect": ""
        }

    def test_get_valid_single_pereval(self):
        response = client.get(
            reverse('submitData-detail', kwargs={'pk': self.pereval.pk}))
        pereval = PerevalAdded.objects.get(pk=self.pereval.pk)
        serializer = PerevalSerializer(pereval)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_pereval(self):
        response = client.get(
            reverse('submitData-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_pereval(self):
        response = client.patch(
            reverse('submitData-detail', kwargs={'pk': self.pereval.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_pereval(self):
        response = client.patch(
            reverse('submitData-detail', kwargs={'pk': self.pereval.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
