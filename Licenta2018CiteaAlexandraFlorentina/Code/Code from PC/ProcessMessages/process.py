import csv
import sys
import os
import django
from django.utils import timezone
from django.conf import settings
from map.models import Incident
from django.core.wsgi import get_wsgi_application

sys.path.append("C://Users//Alexandra Citea//Desktop//Licenta//accidents")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "accidents.settings")
django.setup()

application = get_wsgi_application()


file_msg = open("C://Users//Alexandra Citea//Desktop//Messages.txt", "r")
previous_line1 = file_msg.read().splitlines()
previous_line = []
for elem in previous_line1:
    if elem != "":
        previous_line.append(elem)
print(previous_line)
file_msg.close()
while True:
    file_msg = open("C://Users//Alexandra Citea//Desktop//Messages.txt", "r")
    line1 = file_msg.read().splitlines()
    line = []
    for elem in line1:
        if elem != "":
            line.append(elem)
    if previous_line != line:
        print(line)
        previous_line = line
        new_accident = line[-1]
        print("New accident info: "+new_accident)
        elements = new_accident.split(' ')
        print(elements)
        model = Incident()
        model.timestamp = timezone.now()
        model.accidentsPriority = elements[0]
        model.latitude = elements[1]
        model.longitude = elements[2]
        model.save()

    file_msg.close()
