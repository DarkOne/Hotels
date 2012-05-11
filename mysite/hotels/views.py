# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.http import HttpResponse
from mysite.hotels.models import City, Hotel, HotelRoom, Country
import datetime

def hello(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
    
def searchy(request):
    city = City.objects.filter(name_eng = 'Amsterdam')
    c = city[0].name
    return render_to_response('searchy.html', {'city_name': c})
    
def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})

def search_form(request):
    return render_to_response('search_form.html')
    
def search(request):
    if 'city' in request.GET and request.GET['city']:
        if 'guests' in request.GET and request.GET['guests']:
            city_to_find = request.GET['city']
            guests = request.GET['guests']
            city = City.objects.filter(name__icontains=city_to_find).order_by("name")[0]
            #hotelroom2 = HotelRoom.objects.raw('SELECT r.* FROM hotels_city c, 
            #   hotels_hotel h, hotels_hotelroom r WHERE c.name = %s ', [q]).order_by("name")
            a = '%'
            add = (city_to_find, a)
            ctr = ''.join(add) 
            #city2 = City.objects.raw('SELECT city.id, country.id, city.name FROM hotels_city city, hotels_country country WHERE country.id = city.country_id AND country.name = %s', [ctr])
            room = HotelRoom.objects.raw('SELECT city.id, hotel.name AS hname, room.name, room.guests_count \
                                    FROM hotels_city city, hotels_hotel hotel, hotels_hotelroom room \
                                    WHERE city.id = hotel.city_id AND hotel.id = room.hotel_id \
                                    AND city.name ILIKE %s AND room.guests_count = %s ORDER BY hname', [ctr, guests])
            room = list(room)
            return render_to_response('search_results.html', {'city': city, 'guests': guests, 'room': room})
        else:
            return HttpResponse('Please submit a search term.')

    else:
        return HttpResponse('Please submit a search term.')
