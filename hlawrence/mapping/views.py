from django.shortcuts import render
from utils.viewtools import *
from django.template import loader
from django.http import HttpResponse, JsonResponse


# Create your views here.

def index(request):

	location_dict = locationgather()
	mapdic, center_long, center_lat = locationdata(location_dict)

	template = loader.get_template('mapping/index.html')

	print (mapdic)
	context = {
		'mapdic': mapdic,
		}

	return HttpResponse(template.render(context, request))



def contribute(request): 
	return render(request, 'mapping/contribute.html', {}) 