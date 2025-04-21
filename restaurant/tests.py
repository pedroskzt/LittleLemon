from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Menu, Booking
from .serializers import BookingSerializer, MenuSerializer
from django.contrib.auth import password_validation, authenticate

# Create your tests here.


class MenuTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(
            title="Ice Cream",
            price="15.99",
            inventory=100
        )

    def test_menu_model(self):
        """Test Menu model attributes
        """
        self.assertEqual(self.menu.title, "Ice Cream")
        self.assertEqual(self.menu.price, "15.99")
        self.assertEqual(self.menu.inventory, 100)


class BookingTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            name="Test User",
            no_of_guests=12,
            bookingDate="2025-04-16"
        )

    def test_booking_model(self):
        """Test Bookings model attributes
        """
        self.assertEqual(self.booking.name, "Test User")
        self.assertEqual(self.booking.no_of_guests, 12)
        self.assertEqual(self.booking.bookingDate, "2025-04-16")


class BookingSerializerTest(TestCase):
    def setUp(self):
        self.booking = Booking(
            name="Test User",
            no_of_guests=12,
            bookingDate="2025-04-16"
        )
        self.booking_serializer = BookingSerializer(instance=self.booking)

    def test_booking_serialized_fields(self):
        """Test fields serialized by BookingSerializer
        """

        data = self.booking_serializer.data
        self.assertEqual(set(data.keys()), set(
            ['id', 'name', 'no_of_guests', 'bookingDate']))

    def test_booking_serialized_data(self):
        """Test data serialized by BookingSerializer
        """

        data = self.booking_serializer.data
        self.assertEqual(data["name"], "Test User")
        self.assertEqual(data["no_of_guests"], 12)
        self.assertEqual(data["bookingDate"], "2025-04-16")


class MenuSerializerTest(TestCase):
    def setUp(self):
        self.menu = Menu(
            title="Ice Cream",
            price="15.99",
            inventory=100
        )
        self.menu_serializer = MenuSerializer(instance=self.menu)

    def test_booking_serialized_fields(self):
        """Test fields serialized by BookingSerializer
        """

        data = self.menu_serializer.data
        self.assertEqual(set(data.keys()), set(
            ['id', 'title', 'price', 'inventory']))

    def test_booking_serialized_data(self):
        """Test data serialized by BookingSerializer
        """

        data = self.menu_serializer.data
        self.assertEqual(data["title"], "Ice Cream")
        self.assertEqual(data["price"], "15.99")
        self.assertEqual(data["inventory"], 100)


class MenuAPITest(APITestCase):
    def setUp(self):
        Menu.objects.create(
            title="Ice Cream",
            price="15.99",
            inventory=100
        )

        Menu.objects.create(
            title="Cake",
            price="11.99",
            inventory=5
        )
        self.url = reverse("menu")

    def test_menu_api_get_response(self):
        """Test Menu API GET response
        """
        response = self.client.get(self.url)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Menu.objects.count())

        data = response.data[0]

        self.assertEqual(set(data.keys()), set(
            ['id', 'title', 'price', 'inventory']))
        self.assertEqual(data["title"], "Ice Cream")
        self.assertEqual(data["price"], "15.99")
        self.assertEqual(data["inventory"], 100)

        data = response.data[1]
        self.assertEqual(set(data.keys()), set(
            ['id', 'title', 'price', 'inventory']))
        self.assertEqual(data["title"], "Cake")
        self.assertEqual(data["price"], "11.99")
        self.assertEqual(data["inventory"], 5)

    def test_single_menu_api_get_response(self):
        """Test SingleMenu API GET response
        """
        first_obj = Menu.objects.first()
        expected_response = {
            'id': first_obj.pk,
            "title": first_obj.title,
            "price": str(first_obj.price),
            "inventory": first_obj.inventory
        }

        response = self.client.get(f"{self.url}{first_obj.pk}")
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(isinstance(data, list))

        self.assertEqual(set(data.keys()), set(
            ['id', 'title', 'price', 'inventory']))
        self.assertEqual(response.data, expected_response)


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.new_user_response = self.client.post('/auth/users/', {
            'username': 'admin',
            'password': 'lemon@123',
            'email': 'admin@example.com'
        }, format='json')
        self.user = User.objects.first()

    def test_new_user_created(self):
        self.assertEqual(self.new_user_response.status_code,
                         status.HTTP_201_CREATED)
        self.assertTrue(self.user is not None)
        self.assertEqual(self.new_user_response.data, {
            'username': self.user.username,
            'email': self.user.email})

    def test_login_success(self):
        response = self.client.post('/auth/token/login/', {
            'username': 'admin',
            'password': 'lemon@123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'auth_token': Token.objects.get(user_id=self.user.pk).key})

    def test_login_wrong_username(self):
        response = self.client.post('/auth/token/login/', {
            'username': 'admn',
            'password': 'lemon@123'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password(self):
        response = self.client.post('/auth/token/login/', {
            'username': 'admin',
            'password': 'lemon123'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookingAPITest(APITestCase):
    def setUp(self):
        Booking.objects.create(
            name="Test User",
            no_of_guests=12,
            bookingDate="2025-04-16 13:00:00"
        )

        Booking.objects.create(
            name="Test User 2",
            no_of_guests=2,
            bookingDate="2025-04-17 19:00:00"
        )

        self.client.post('/auth/users/', {
            'username': 'admin',
            'password': 'lemon@123',
            'email': 'admin@example.com'
        }, format='json')

        response = self.client.post('/auth/token/login/', {
            'username': 'admin',
            'password': 'lemon@123'
        }, format='json')

        self.user_token = response.data['auth_token']

    def test_booking_api_get_response_list(self):
        """Test Menu API GET (list) response
        """
        url = reverse("booking-list")
        response = self.client.get(
            url, headers={"Authorization": f"Token {self.user_token}"})
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Booking.objects.count())

        data = response.data[0]

        self.assertEqual(set(data.keys()), set(
            ['id', 'name', 'no_of_guests', 'bookingDate']))
        self.assertEqual(data["name"], "Test User")
        self.assertEqual(data["no_of_guests"], 12)
        self.assertEqual(data["bookingDate"], "2025-04-16T13:00:00Z")

        data = response.data[1]
        self.assertEqual(set(data.keys()), set(
            ['id', 'name', 'no_of_guests', 'bookingDate']))
        self.assertEqual(data["name"], "Test User 2")
        self.assertEqual(data["no_of_guests"], 2)
        self.assertEqual(data["bookingDate"], "2025-04-17T19:00:00Z")
