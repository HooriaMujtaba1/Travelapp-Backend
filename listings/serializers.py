from rest_framework import serializers
from .models import Listing, ListingImage, Booking
from datetime import datetime

# Listing Image Serializer to handle image data for listings
class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image']  # Returns the image URL in JSON


# Listing Serializer to handle listing details, including related images
class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)  # Read-only images field

    class Meta:
        model = Listing
        fields = ['id', 'name', 'location_url', 'images']


# Booking Serializer to handle booking data, including associated listing details
class BookingSerializer(serializers.ModelSerializer):
    listing_id = serializers.IntegerField(write_only=True)  # Write-only field for listing ID
    listing_details = ListingSerializer(source='listing', read_only=True)  # Read-only field for listing details

    class Meta:
        model = Booking
        fields = ['id', 'listing_id', 'listing_details', 'start_date', 'end_date', 'created_at']
        read_only_fields = ['id', 'created_at', 'listing_details']  # Fields that should not be writable

    def validate(self, data):
        # Ensure start_date is before end_date
        start_date = data['start_date']
        end_date = data['end_date']

        # Convert strings to datetime objects if necessary
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%d/%m/%Y")  # Convert start_date from dd/mm/yyyy format
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%d/%m/%Y")  # Convert end_date from dd/mm/yyyy format

        # Validate date range
        if start_date > end_date:
            raise serializers.ValidationError("Start date must be before end date.")

        request = self.context.get('request')
        user = request.user if request else None

        # Check if the user is authenticated and if they own the listing
        if user and user.is_authenticated:
            try:
                listing = Listing.objects.get(id=data['listing_id'], user=user)  # Ensure the listing belongs to the user
            except Listing.DoesNotExist:
                raise serializers.ValidationError("Listing not found or does not belong to you.")
        else:
            # For anonymous users, just check if the listing exists
            try:
                listing = Listing.objects.get(id=data['listing_id'])
            except Listing.DoesNotExist:
                raise serializers.ValidationError("Listing not found.")

        data['listing'] = listing  # Attach the Listing instance to the booking
        return data

    def create(self, validated_data):
        validated_data.pop('listing_id', None)  # Remove listing_id as it's already included in the listing field

        # Assign user to booking if authenticated
        user = self.context['request'].user if self.context['request'] else None
        validated_data['user'] = user

        # Create the booking object
        return super().create(validated_data)
