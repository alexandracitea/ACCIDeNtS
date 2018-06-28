from django.contrib import admin
from .models import Incident
from .models import Unit

admin.site.register(Incident)
admin.site.register(Unit)