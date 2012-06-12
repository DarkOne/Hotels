from django.contrib import admin
from mysite.hotels.models import City, Hotel, HotelRoom, Country, Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'guest_name', 'check_in', 'check_out')
    search_fields = ('room',)
    raw_id_fields = ('room',)

admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(HotelRoom)
admin.site.register(Country)
admin.site.register(Booking, BookingAdmin)
