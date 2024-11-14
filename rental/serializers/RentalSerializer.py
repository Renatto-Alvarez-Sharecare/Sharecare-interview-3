from rest_framework import serializers
from rental.models import Rental
from rental.serializers.CarSerializer import CarSerializer
from rental.serializers.CustomerSerializer import CustomerSerializer


class RentalSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Rental
        fields = ['id', 'car', 'customer', 'rental_date', 'return_date']
