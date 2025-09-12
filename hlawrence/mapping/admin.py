from django.contrib import admin

from .models import Location, Haunting, Hauntingtype

admin.site.register(Location)
admin.site.register(Haunting)
admin.site.register(Hauntingtype)
