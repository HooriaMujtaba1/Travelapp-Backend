# listings/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ListingViewSet, BookingViewSet
from .views import create_admin

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('create-admin/', create_admin),
    path('', include(router.urls)),
]
