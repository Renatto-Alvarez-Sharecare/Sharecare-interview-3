from django.urls import path
from rental.handlers.rental_handler import CarRentalHandler

handler = CarRentalHandler.as_view()

urlpatterns = [
    path('cars/available/', handler, name='list_available_cars'),
    path('rent-car/<int:car_id>/<int:customer_id>/', handler, name='rent_car'),
    path('return-car/<int:rental_id>/', handler, name='return_car'),
]
