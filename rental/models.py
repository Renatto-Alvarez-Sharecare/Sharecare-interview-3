from django.db import models
from django.utils import timezone


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    is_rented = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.make} {self.model}"


class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def return_car(self):
        self.car.is_rented = True
        self.car.save()
        self.save()
