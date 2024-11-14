from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rental.models import Car, Customer, Rental
from rental.serializers.CarSerializer import CarSerializer


class CarRentalHandler(APIView):
    def get(self, request):
        # List available cars (GET /api/cars/available/)
        available_cars = Car.objects.filter(is_rented=False)
        serializer = CarSerializer(available_cars, many=True)
        return Response(serializer.data)

    def post(self, request, car_id, customer_id):
        # Rent a car (POST /api/rent-car/{car_id}/{customer_id}/)
        car = get_object_or_404(Car, id=car_id)
        customer = get_object_or_404(Customer, id=customer_id)

        if not car.is_rented:
            Rental.objects.create(car=car, customer=customer)
            car.is_rented = False
            car.save()
            return Response({"message": "Car rented successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Car is already rented."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, rental_id):
        # Return a car (PUT /api/return-car/{rental_id}/)
        rental = get_object_or_404(Rental, id=rental_id)

        if rental.return_date is None:
            rental.return_car()
            return Response({"message": "Car returned successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Car was already returned."}, status=status.HTTP_400_BAD_REQUEST)
