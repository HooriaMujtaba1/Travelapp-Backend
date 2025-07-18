from rest_framework import serializers
from .models import Listing, ListingImage, Booking
from datetime import datetime

# Serializer for listing images
class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image']


# Serializer for listings
class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'name', 'location_url', 'images']


# Serializer for bookings
class BookingSerializer(serializers.ModelSerializer):
    listing_id = serializers.IntegerField(write_only=True)
    listing_details = ListingSerializer(source='listing', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'listing_id', 'listing_details', 'start_date', 'end_date', 'created_at']
        read_only_fields = ['id', 'created_at', 'listing_details']

    def validate(self, data):
        start_date = data['start_date']
        end_date = data['end_date']

        # Optional: parse date strings if needed
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        if start_date > end_date:
            raise serializers.ValidationError("Start date must be before end date.")

        listing_id = data.get('listing_id')
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            raise serializers.ValidationError("Listing not found.")

        data['listing'] = listing
        return data

    def create(self, validated_data):
        validated_data.pop('listing_id', None)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
