# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from mysite.hotels.models import City
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
        q = request.GET['q']
        city = City.objects.filter(name_eng__icontains=q)
        return render_to_response('search_results.html',
            {'city': city, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')
