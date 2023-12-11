import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from venueapi.models import Band
from django.contrib.auth.models import User

class BandTests(APITestCase):

    fixtures = ['users', 'tokens', 'bands']

    def setUp(self) -> None:
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_band(self):

        url = '/bands'
        data = {
            "name": "Test Name",
            "genre": "Test Genre"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response['name'], 'Test Name')
        self.assertEqual(json_response['genre'], 'Test Genre')