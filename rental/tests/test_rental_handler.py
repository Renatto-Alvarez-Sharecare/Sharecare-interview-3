from django.test import TestCase
from rental.models import Car, Customer, Rental
from rest_framework.test import APIClient
from rest_framework import status


class CarRentalAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.car1 = Car.objects.create(make="Tesla", model="Model S", is_rented=False)
        self.car2 = Car.objects.create(make="Honda", model="Civic", is_rented=False)
        self.customer = Customer.objects.create(name="Alice")

    # Test listing available cars
    def test_list_available_cars(self):
        response = self.client.get('/rental/cars/available/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn("Tesla", str(response.data))

    # Test renting a car
    def test_rent_car(self):
        response = self.client.post(f'/rental/rent-car/{self.car1.id}/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.car1.refresh_from_db()
        self.assertTrue(self.car1.is_rented)

    # Test returning a car
    def test_return_car(self):
        rental = Rental.objects.create(car=self.car1, customer=self.customer)
        response = self.client.put(f'/rental/return-car/{rental.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car1.refresh_from_db()
        self.assertFalse(self.car1.is_rented)

    # Renting a car that's already rented
    def test_rent_already_rented_car(self):
        self.car1.is_rented = True
        self.car1.save()

        response = self.client.post(f'/rental/rent-car/{self.car1.id}/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Car is already rented", response.data['error'])

    # Returning a car that was already returned
    def test_return_already_returned_car(self):
        rental = Rental.objects.create(car=self.car1, customer=self.customer)
        rental.return_car()  # Mark the car as returned

        response = self.client.put(f'/rental/return-car/{rental.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Car was already returned", response.data['error'])

    # Renting a car with an invalid customer ID
    def test_rent_car_invalid_customer(self):
        response = self.client.post(f'/rental/rent-car/{self.car1.id}/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Not Found", response.data['detail'])

    # Renting a car with an invalid car ID
    def test_rent_car_invalid_car(self):
        response = self.client.post(f'/rental/rent-car/999/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("not_found", response.data['detail'].code)

    # Returning a car that hasn't been rented
    def test_return_non_rented_car(self):
        response = self.client.put(f'/rental/return-car/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Not Found", response.data['detail'])
