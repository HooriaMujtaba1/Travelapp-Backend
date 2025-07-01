from django.db import models
from django.conf import settings

class Listing(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255)
    location_url = models.URLField(
        max_length=500,
        help_text="https://maps.google.com/"
    )

    def __str__(self):
        return self.name

    # Optional: Prevent booking overlap at the database level by unique constraint
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_listing')
        ]


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='listing_images/')

    def __str__(self):
        return f"Image for {self.listing.name}"


class Booking(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} booked {self.listing.name} from {self.start_date} to {self.end_date}"

    # Optional: Add constraint to prevent overlapping bookings
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['listing', 'start_date', 'end_date'], name='unique_booking_dates')
        ]
