import csv
import sys
import os
import django

sys.path.append(os.path.join(os.path.dirname(__file__), 'accidents'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "accidents.settings")
from django.conf import settings

from accidents.models import MyModel

file_msg = open("C://Users//Alexandra Citea//Desktop//Messages.txt", "r")
previous_line1 = file_msg.read().splitlines()
previous_line=[]
for elem in previous_line1:
    if elem != "":
        previous_line.append(elem)
print (previous_line)
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
        with open("C://Users//Alexandra Citea//Desktop//MessagesToBeInserted.txt", "w+") as file:
            wr = csv.writer(file, quoting = csv.QUOTE_ALL)
            wr.writerow(elements)
        file.close()
    file_msg.close()
