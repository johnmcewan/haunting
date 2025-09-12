from django.shortcuts import render

# Create your views here.

def index(request): 
    return render(request, 'mapping/index.html', {}) 

def contribute(request): 
    return render(request, 'mapping/contribute.html', {}) 