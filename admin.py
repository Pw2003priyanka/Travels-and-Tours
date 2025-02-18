from django.contrib import admin
from .models import package,travel_agency



# Register your models here.
admin.site.register(travel_agency)
admin.site.register(package)

