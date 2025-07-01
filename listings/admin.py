from django.contrib import admin
from django.utils.html import format_html
from .models import Listing, ListingImage, Booking
from django.contrib import admin

# Unregister auto-registered models
try:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
    admin.site.unregister(BlacklistedToken)
    admin.site.unregister(OutstandingToken)
except (ImportError, admin.sites.NotRegistered):
    pass

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1  # Number of extra blank image upload forms displayed


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'location_url', 'image_count']
    search_fields = ['name', 'location_url', 'user__username', 'user__email']
    readonly_fields = ['map_preview']
    fields = ['name', 'user', 'location_url', 'map_preview']  # Added user here
    inlines = [ListingImageInline]

    def image_count(self, obj):
        """Display how many images are attached to this listing."""
        return obj.images.count()
    image_count.short_description = 'Image Count'

    def map_preview(self, obj):
        """Embed a Google map iframe preview if valid coordinates found."""
        if obj and obj.location_url:
            import re
            match = re.search(r'@([-0-9.]+),([-0-9.]+)', obj.location_url)
            if match:
                lat, lng = match.groups()
                embed_url = f"https://maps.google.com/maps?q={lat},{lng}&z=15&output=embed"
                return format_html(
                    '<iframe width="100%" height="300" src="{}" frameborder="0" '
                    'style="border:0;" allowfullscreen></iframe>',
                    embed_url
                )
        return "No valid coordinates or embeddable map URL found."


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing', 'user', 'start_date', 'end_date', 'created_at']
    search_fields = ['listing__name', 'user__email', 'user__username']
    list_filter = ['start_date', 'end_date', 'created_at', 'user']
    ordering = ['-created_at']
