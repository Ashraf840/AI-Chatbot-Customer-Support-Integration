from django.urls import path
from .views import calculate_da, calculate_ta_da, calculate_ta

urlpatterns = [
    path('calculate_da/', calculate_da, name='calculate_da'),
    path('calculate_ta/', calculate_ta, name='calculate_ta'),
    path('calculate_ta_da/', calculate_ta_da, name='calculate_ta_da'),
]

