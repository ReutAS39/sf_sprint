import json

from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pereval.models import PerevalAdded, PerevaladdedImages, Images, Users, Coords, Level
from pereval.serializers import PerevalSerializer

client = Client()

valid_data = {
            "user": {
                "email": "test@mail.ru",
                "phone": "+79216340667",
                "fam": "Сергеевич",
                "name": "Александр",
                "otc": "Сергеевич"
            },
            "coords": {
                "latitude": 32.1,
                "longitude": 48.2,
                "height": 4892
            },
            "level": {
                "mark": "2Б"
            },
            "images": [
                {
                    "data": "http://127.0.0.1:8000/photos/2023/04/11/19._%D0%A1%D0%B0%D0%BC%D0%BE%D0%BB%D0%B5%D1%82%D1%8B.jpg",
                    "title": "Вид с вершины"
                },
                {
                    "data": "https://proprikol.ru/wp-content/uploads/2020/08/krasivye-kartinki-kotikov-36.jpg",
                    "title": "Вид с перевала"
                }
            ],
            "beauty_title": "пер.",
            "title": "Мао",
            "other_titles": "--",
            "connect": "Уллу-Тау"
        }


invalid_data = {
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
                'mark': 'dfdf',
            },
            'images': [
                {
                    'title': 'Test Image',
                    'img': 'test.jpg'
                }
            ]
        }


class CreateNewPerevalTest(APITestCase):
    """ Test module for inserting a new pereval """

    def test_create_valid_pereval(self):

        response = client.post(
            reverse('pereval-add'),
            data=valid_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_pereval(self):

        response = client.post(
            reverse('pereval-add'),
            data=invalid_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetPatchSinglePerevalTest(APITestCase):
    """ Test module for GET and PATCH single pereval API """
    def setUp(self):
        self.level = Level.objects.create(mark='1Б')
        self.coords = Coords.objects.create(latitude=33.3, longitude=55.5, height=777)
        self.user = Users.objects.create(email='test@test.ru', phone='+79521542323', name='Тест', fam='Тес', otc='Тест')
        self.image = Images.objects.create(title='Тест заголовок', data='https://test.ru/uploads/2020/08/test-36.jpg')
        self.pereval = PerevalAdded.objects.create(user=self.user, coords=self.coords, level=self.level)
        self.perevalimages = PerevaladdedImages.objects.create(images=self.image, perevaladded=self.pereval)

    def test_get_valid_single_pereval(self):
        response = client.get(
            reverse('pereval-detail', kwargs={'id': self.pereval.id}))
        pereval = PerevalAdded.objects.get(pk=self.pereval.pk)
        serializer = PerevalSerializer(pereval)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_pereval(self):
        response = client.get(
            reverse('pereval-detail', kwargs={'id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_pereval(self):
        response = client.patch(
            reverse('pereval-update', kwargs={'id': self.pereval.id}),
            data=json.dumps(valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_pereval(self):
        response = client.patch(
            reverse('pereval-update', kwargs={'id': self.pereval.id}),
            data=json.dumps(invalid_data),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
