from django.db import models

# Create your models here.


    
class Country(models.Model):
    name = models.TextField()
    name_eng = models.TextField()
    is_favorite = models.BooleanField()
    visa_support = models.BooleanField()
    currency = models.CharField(max_length=3)
    
    def __unicode__(self):
        return u'%s' % (self.name) 
    
class City(models.Model):
    name = models.TextField()
    name_eng = models.TextField()
    is_capital = models.BooleanField()
    is_favorite = models.BooleanField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.ForeignKey(Country)
    
    def __unicode__(self):
        return u'%s' % (self.name) 
    
class Hotel(models.Model):
    city = models.ForeignKey(City)
    country = models.ForeignKey(Country)
    name = models.TextField()
    star_rating = models.DecimalField(max_digits=2, decimal_places=1)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    telephone = models.TextField()
    fax = models.TextField()
    email = models.EmailField(max_length=100)
    web = models.URLField()
    location = models.TextField()
    report_location = models.TextField()
    report_direction = models.TextField()
    report_general = models.TextField()
    report_rooms = models.TextField()
    report_exterior = models.TextField()
    report_lobby = models.TextField()
    report_restaurant = models.TextField()
    
    def __unicode__(self):
        return u'%s' % (self.name) 

class HotelRoom(models.Model):
    name = models.CharField(max_length=32)
    hotel = models.ForeignKey(Hotel)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    guests_count = models.SmallIntegerField()
    def __unicode__(self):
        return u'%s' % (self.name)    

class Booking(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    room = models.ForeignKey(HotelRoom)
    guest_name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return u'%s %s' % (self.room, self.guest_name)
