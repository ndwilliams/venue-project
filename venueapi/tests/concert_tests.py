import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from venueapi.models import Concert, Band, Venue, Opener
from django.contrib.auth.models import User

class ConcertTests(APITestCase):

    fixtures = ['users', 'tokens', 'concerts', 'bands', 'venues', 'openers']

    def setUp(self) -> None:
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_get_concert(self):

        band = Band.objects.get(id=1)
        venue = Venue.objects.get(id=2)

        concert = Concert()
        concert.band = band
        concert.venue = venue
        concert.doors_open = "2023-12-25T19:00:00.158Z"
        concert.show_starts = "2023-12-25T20:00:00.158Z"
        concert.active = True
        concert.save()

        response = self.client.get(f'/concerts/{concert.id}')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['doors_open'], "2023-12-25T19:00:00.158000Z")
        self.assertEqual(json_response['show_starts'], "2023-12-25T20:00:00.158000Z")
        self.assertEqual(json_response['active'], True)

    def test_get_all_concerts(self):

        response = self.client.get('/concerts')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(json_response, list)

        for obj in json_response:
            self.assertIn("band", obj)
            self.assertIn("venue", obj)
            self.assertIn("opening_bands", obj)
            self.assertIn("doors_open", obj)
            self.assertIn("show_starts", obj)
            self.assertIn("active", obj)

    def test_create_concert(self):

        url = "/concerts"
        data = {
            "band": 1,
            "venue": 1,
            "doors_open": "2023-12-25T19:00:00.158Z",
            "show_starts": "2023-12-25T20:00:00.158Z", 
            "active": True
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response['band']['id'], 1)
        self.assertEqual(json_response['venue']['id'], 1)
        self.assertEqual(json_response['doors_open'], "2023-12-25T19:00:00.158Z")
        self.assertEqual(json_response['show_starts'], "2023-12-25T20:00:00.158Z")
        self.assertEqual(json_response['active'], True)

    # def test_update_concert(self):

    #     band = Band.objects.get(id=1)
    #     venue = Venue.objects.get(id=1)

    #     concert = Concert()
    #     concert.band = band
    #     concert.venue = venue
    #     concert.doors_open = "2023-12-25T19:00:00.158Z"
    #     concert.show_starts = "2023-12-25T20:00:00.158Z"
    #     concert.active = True
    #     concert.save()

    #     data = {
    #         "band": {"id" : 2},
    #         "venue": {"id" : 2},
    #         "doors_open": "2023-12-25T19:30:00.158Z",
    #         "show_starts": "2023-12-25T21:00:00.158Z",
    #         "active": False,
    #         "opening_bands": [{"id": 4}, {"id": 5}]        
    #     }

    #     response = self.client.put(f'/concerts/{concert.id}', data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, f"Expected 200 OK but received{response.status_code}. Content: {response.content}")

    #     response = self.client.get(f'concerts/{concert.id}')
    #     json_response = json.loads(response.content)

    #     self.assertEqual(json_response['band']['id'], 2)
    #     self.assertEqual(json_response['venue']['venue'], 2)
    #     self.assertEqual(json_response['doors_open'], "2023-12-25T19:30:00.158000Z")
    #     self.assertEqual(json_response['show_starts'], "2023-12-25T21:00:00.158000Z")
    #     self.assertEqual(json_response['active'], False)
    #     self.assertIsInstance(json_response, dict)


