# === Django REST Framework Imports ===
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import JsonResponse
# === Django Imports ===
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as DefaultUser  # For fallback superuser creation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse

# === Local App Imports ===
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

# === Get the custom user model ===
User = get_user_model()


# === ViewSet: ListingViewSet ===
class ListingViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Listing instances.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# === APIView: PasswordResetConfirmView (POST) ===
class PasswordResetConfirmView(APIView):
    """
    POST endpoint to confirm password reset using UID and token.

    Expected Payload:
    - id (Base64 encoded UID)
    - token (Password reset token)
    - new_password (The new password)
    """

    def post(self, request):
        uidb64 = request.data.get('id')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not uidb64 or not token or not new_password:
            return Response(
                {'error': 'Missing id (uidb64), token, or new_password.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response(
                {'error': 'Invalid or non-existent user.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response(
                {'error': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {'status': 'Password has been reset successfully.'},
            status=status.HTTP_200_OK
        )


# === ViewSet: BookingViewSet ===
class BookingViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and creating Booking instances.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


# === Custom Admin Creation View ===
def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        return JsonResponse({'message': 'Admin user created'})
    return JsonResponse({'message': 'Admin already exists'})
