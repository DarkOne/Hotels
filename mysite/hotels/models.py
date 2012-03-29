from django.db import models

# Create your models here.


    
class Country(models.Model):
    name = models.TextField()
    name_eng = models.TextField()
    is_favourite = models.BooleanField()
    visa_support = models.BooleanField()
    currency = models.CharField(max_length=3)
    
class City(models.Model):
    name = models.TextField()
    name_eng = models.TextField()
    is_capital = models.BooleanField()
    is_favorite = models.BooleanField()
    latitude = models.TextField()
    longitude = models.TextField()
    country_id = models.ForeignKey(Country)
    
class Hotels(models.Model):
    city_id = models.ForeignKey(City)
    country_id = models.ForeignKey(Country)
    category = models.IntegerField()
    name = models.TextField()
    star_rating = models.DecimalField(max_digits=2, decimal_places=1)
    customer_rating = models.DecimalField(max_digits=2, decimal_places=1)
    address = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    telephone = models.TextField()
    fax = models.TextField()
    email = models.EmailField()
    web = models.URLField()
    location = models.TextField()
    report_location = models.TextField()
    report_direction = models.TextField()
    report_general = models.TextField()
    report_rooms = models.TextField()
    report_exterior = models.TextField()
    report_lobby = models.TextField()
    report_restaurant = models.TextField()
    
class HotelRoom(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    guests_count = models.SmallIntegerField()    
