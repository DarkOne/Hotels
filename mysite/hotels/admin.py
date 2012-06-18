from django.contrib import admin
from mysite.hotels.models import City, Hotel, HotelRoom, Country, Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'guest_name', 'check_in', 'check_out')
    search_fields = ('room',)
    raw_id_fields = ('room',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'price', 'guests_count')
    #ordering = ('hotel', 'name')
    search_fields = ('name', 'hotel__name', 'hotel__city__name')
    raw_id_fields = ('hotel',)

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')
    search_fields = ('name', 'city__name', 'country__name')
    #raw_id_fields = ('hotel',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    ordering = ('name',)

admin.site.register(City, CityAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelRoom, RoomAdmin)
admin.site.register(Country)
admin.site.register(Booking, BookingAdmin)
