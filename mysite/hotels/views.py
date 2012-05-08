# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from mysite.hotels.models import City, Hotel, HotelRoom
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
    if 'q' in request.GET and request.GET['q']:
        if 'n' in request.GET and request.GET['n']:
            q = request.GET['q']
            n = request.GET['n']
            city = City.objects.filter(name__icontains=q).order_by("name")
            city_id = city[0].id
            hotel = Hotel.objects.filter(city_id = city_id).order_by("name")
            hotel_id = hotel[0].id
            
            hotelroom = HotelRoom.objects.filter(hotel_id = hotel_id).order_by("name")
            #hotelroom2 = HotelRoom.objects.raw('SELECT r.* FROM hotels_city c, 
             #   hotels_hotel h, hotels_hotelroom r WHERE c.name = %s', [q]).order_by("name")
            
            return render_to_response('search_results.html',
                {'hotel': hotel, 'query': city[0].name, 'hotelroom': hotelroom, 'hotelname': hotel[0].name})
        else:
            return HttpResponse('Please submit a search term.')

    else:
        return HttpResponse('Please submit a search term.')
