# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.context_processors import csrf
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

def booking_1(request):
    room = request.POST
    if 'room_id' in room and 'room_name' in room and 'hotel_name' in room and 'city_name' in room and 'in' in room and 'out' in room:
        room_id = room['room_id']
        room_name = room['room_name']
        hotel_name = room['hotel_name']
        city_name = room['city_name']
        check_in = room['in']
        check_out = room['out']
        c = {'room_id': room_id, 'room_name': room_name, 'hotel_name': hotel_name, 'city_name': city_name, 'in': check_in, 'out': check_out}
        c.update(csrf(request))
        return render_to_response('booking_1.html', c)
        #now = datetime.date.isoformat(datetime.datetime.now())
        #return render_to_response('current_datetime.html', {'current_datetime': now})
    else:
        return HttpResponse('Error')
        
def booking_2(request):
    room = request.POST
    now = datetime.date.isoformat(datetime.datetime.now())
    if 'room_id' in room and 'in' in room and 'out' in room and 'name' in room:
        room_id = room['room_id']
        check_in = room['in']
        check_out = room['out']
        name = room['name']
        room_name = room['room_name']
        hotel_name = room['hotel_name']
        city_name = room['city_name']
        room = Booking(room_id = room_id, guest_name = name, check_in = check_in, check_out = check_out)
        room.save()
        now = datetime.date.isoformat(datetime.datetime.now())
        c = {'room_name': room_name, 'hotel_name': hotel_name, 'city_name': city_name, 'name': name, 'in': check_in, 'out': check_out}
        c.update(csrf(request))
        return render_to_response('booking_2.html', c)
    else:
        return HttpResponse('Error')

def search(request):
    if 'city' in request.GET and request.GET['city']:
        if 'guests' in request.GET and request.GET['guests']:
            if 'in' in request.GET and 'out' in request.GET and request.GET['in'] < request.GET['out']:
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
                room = HotelRoom.objects.raw('SELECT city.id, hotel.name AS hname, room.name, room.id, room.guests_count \
                                        FROM hotels_city city, hotels_hotel hotel, hotels_hotelroom room \
                                        WHERE city.id = hotel.city_id AND hotel.id = room.hotel_id \
                                        AND city.name ILIKE %s AND room.guests_count = %s \
                                        AND NOT EXISTS \
                                        (SELECT 1 FROM hotels_booking booking WHERE booking.room_id = room.id \
                                        AND ((%s >= booking.check_in AND %s < booking.check_out) \
                                        OR (%s > booking.check_in AND %s <= booking.check_out) \
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
                c = {'city': city, 'guests': guests, 'count': count, 'rooms': rooms, 'in': check_in, 'out': check_out}
                c.update(csrf(request))
                return render_to_response('search_results.html', c)
            else:
                return HttpResponse('Проверьте даты.')
        else:
            return HttpResponse('Выберите количество гостей.')

    else:
        return HttpResponse('Проверьте искомый город.')
