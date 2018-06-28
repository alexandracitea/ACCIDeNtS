from django.shortcuts import render
from django.http import HttpResponse
from .models import Incident
from .models import Unit
from django.template import loader


def index(request):
    all_incidents = Incident.objects.all()
    all_units = Unit.objects.all()
    template = loader.get_template('map/mainPage.html')
    context = {
        'all_incidents':all_incidents,
        'all_units' : all_units
    }
    return HttpResponse(template.render(context,request))

def splitAccidents(request):
    ordered_incidents = Incident.objects.filter().order_by('accidentsPriority')
    template = loader.get_template('map/accidents.html')
    context = {
        'ordered_incidents' : ordered_incidents,
    }
    return HttpResponse(template.render(context, request))

def detail(request, incident_id):
    template = loader.get_template('map/specificAccident.html')
    all_units = Unit.objects.all()
    specific_incident = Incident.objects.filter(id=incident_id)
    context = {
        'specific_incident': specific_incident,
        'all_units': all_units,
    }
    return HttpResponse(template.render(context, request))
