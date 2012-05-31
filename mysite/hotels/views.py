# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.http import HttpResponse
from mysite.hotels.models import City, Hotel, HotelRoom, Country, Booking
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
    now = datetime.date.isoformat()
    return render_to_response('current_datetime.html', {'current_datetime': now})

def search_form(request):
    now = datetime.date.isoformat(datetime.datetime.now())
    return render_to_response('search_form.html', {'now': now})
    
def search(request):
    if 'city' in request.GET and request.GET['city']:
        if 'guests' in request.GET and request.GET['guests']:
            city_to_find = request.GET['city']
            guests = request.GET['guests']
            check_in = request.GET['in']
            check_out = request.GET['out']
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
                                    AND city.name ILIKE %s AND room.guests_count = %s \
                                    AND NOT EXISTS \
                                    (SELECT 1 FROM hotels_booking booking WHERE booking.room_id = room.id \
                                    AND ((%s > booking.check_in AND %s < booking.check_out) \
                                    OR (%s > booking.check_in AND %s < booking.check_out) \
                                    OR (%s < booking.check_in AND %s > booking.check_out) )) \
                                    ORDER BY hname', [ctr, guests, check_in, check_in, check_out, check_out, check_in, check_out])
            room = list(room)
            count = len(room)
            hotel = ''
            rooms = []
            for i in room:
                if hotel != i.hname:
                    rooms.append(i.hname)
                    hotel = i.hname
                rooms.append(i)
            l = len(rooms)           
            
            return render_to_response('search_results.html', {'city': city, 'guests': guests, 'count': count, 'rooms': rooms, 'in': check_in, 'out': check_out})
        else:
            return HttpResponse('Выберите количество гостей.')

    else:
        return HttpResponse('Проверьте искомый город.')
