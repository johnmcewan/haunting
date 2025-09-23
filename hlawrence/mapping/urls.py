# urls.py
from django.urls import path
from . import views

app_name = 'mapping'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('map/', views.map, name ='map'),
    path('haunting/', views.haunting_search, name='haunting'),
    path('about/', views.about, name='about'),
    path('story/', views.submitstory, name='submitstory'),
    path('credit/', views.credit, name='credit'),
    
    # Story detail page
    path('haunting/<int:story_id>/', views.haunting_detail, name='haunting_detail'),
    
    # API endpoints
    path('api/haunting/', views.get_haunting_json, name='haunting_api'),
    
    # Legacy URL (if you had a contribute page)
    path('contribute/', views.submitstory, name='contribute'),  # Redirect to submitstory
]