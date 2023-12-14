import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from venueapi.models import Venue
from django.contrib.auth.models import User

class VenueTests(APITestCase):

    fixtures = ['users', 'tokens', 'venues']

    def setUp(self) -> None:
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_create_venue(self):

        url = "/venues"
        data = {
            "venue_outside_image_url": "www.outsideimageurl.com",
            "venue_inside_image_url": "www.insideimageurl.com",
            "name": "Venue Name",
            "address": "112 Venue Ave, Nashville TN, 45061",
            "capacity": 312,
            "about_section": "lorem ipsum",
            "active": True
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response['venue_outside_image_url'], "www.outsideimageurl.com")
        self.assertEqual(json_response['venue_inside_image_url'], "www.insideimageurl.com")
        self.assertEqual(json_response['name'], "Venue Name")
        self.assertEqual(json_response['address'], "112 Venue Ave, Nashville TN, 45061")
        self.assertEqual(json_response['capacity'], 312)
        self.assertEqual(json_response['about_section'], "lorem ipsum")
        self.assertEqual(json_response['active'], True)

    def test_get_all_venues(self):
        response = self.client.get(f'/venues')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(json_response, list)

        for obj in json_response:
            self.assertIn("venue_outside_image_url", obj)
            self.assertIn("venue_inside_image_url", obj)
            self.assertIn("name", obj)
            self.assertIn("address", obj)
            self.assertIn("capacity", obj)
            self.assertIn("about_section", obj)
            self.assertIn("active", obj)
                
    def test_get_venue(self):
        venue = Venue()
        venue.venue_outside_image_url = "www.outsideimage.com"
        venue.venue_inside_image_url = "www.insideimage.com"
        venue.name = "Venue Name"
        venue.address = "Venue Address Test"
        venue.capacity = 222
        venue.about_section = "lorem ipsum"
        venue.active = True
        venue.save()

        response = self.client.get(f'/venues/{venue.id}')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["venue_outside_image_url"], "www.outsideimage.com")
        self.assertEqual(json_response["venue_inside_image_url"], "www.insideimage.com")
        self.assertEqual(json_response['name'], "Venue Name")
        self.assertEqual(json_response['address'], "Venue Address Test")
        self.assertEqual(json_response['capacity'], 222)
        self.assertEqual(json_response['about_section'], "lorem ipsum")
        self.assertEqual(json_response['active'], True)
        self.assertIsInstance(json_response, dict)

    def test_change_venue(self):

        venue = Venue()
        venue.venue_outside_image_url = "http://www.outsideimage.com"
        venue.venue_inside_image_url = "http://www.insideimage.com"
        venue.name = "Venue Name"
        venue.address = "Venue Address Test"
        venue.capacity = 222
        venue.about_section = "lorem ipsum"
        venue.active = True
        venue.save()

        data = {  
            "venue_outside_image_url": "http://www.newoutsideimageurl.com",
            "venue_inside_image_url": "http://www.newinsideimageurl.com",
            "name": "New Venue Name",
            "address": "New Venue Address",
            "capacity": 313,
            "about_section": "new lorem ipsum",
            "active": False
        }

        response = self.client.put(f'/venues/{venue.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Expected 200 OK but received {response.status_code}. Content: {response.content}")

        response = self.client.get(f'/venues/{venue.id}')
        json_response = json.loads(response.content)

        self.assertEqual(json_response["venue_outside_image_url"], "http://www.newoutsideimageurl.com")
        self.assertEqual(json_response["venue_inside_image_url"], "http://www.newinsideimageurl.com")
        self.assertEqual(json_response['name'], "New Venue Name")
        self.assertEqual(json_response['address'], "New Venue Address")
        self.assertEqual(json_response['capacity'], 313)
        self.assertEqual(json_response['about_section'], "new lorem ipsum")
        self.assertEqual(json_response['active'], False)
        self.assertIsInstance(json_response, dict)
