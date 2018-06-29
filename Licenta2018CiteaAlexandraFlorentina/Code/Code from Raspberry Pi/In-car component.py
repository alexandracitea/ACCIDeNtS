import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
import sqlite3
import serial
import RPi.GPIO as GPIO     
import os, time

connection = sqlite3.connect('codes.db')
cursor = connection.execute('SELECT id, currenttime, speed, rpm, airtemperature, oiltemperature FROM rawcodes WHERE id=(SELECT MAX(id) FROM rawcodes)');
for row in cursor:
    print ("ID = " + str(row[0]));
    print ("Time = " + str(row[1]));
    print ("Speed = " + str(row[2]));
    speed = str(row[2]).split();
    if speed[3] == "41" and speed[4] == "0D":
        speedToBeInserted = int(speed[5], 16)
	print("Calculated speed: " + str(speedToBeInserted));
    print ("RPM = " + str(row[3]));
    rpm = str(row[3]).split();
    if rpm[3] == "41" and rpm[4] == "0C":
	rpmToBeInserted = int(rpm[5]+rpm[6],16)
	print("Calculated RPM: " + str(rpmToBeInserted));
    print ("Air Temperature = " + str(row[4]));
    airtemp = str(row[4]).split();
    if airtemp[3] == "41" and airtemp[4] == "46":
	airtempToBeInserted = int(airtemp[5],16)
	print("Calculated air temperature: " +str(airtempToBeInserted));
    print ("Oil Temperature = " + str(row[5]));
    oiltemp = str(row[5]).split();
    if oiltemp[3] == "41" and oiltemp[4] == "5C":
	oiltempToBeInserted = int(oiltemp[5],16)
	print("Calculated oil temperature: " + str(oiltempToBeInserted));
    if str(speedToBeInserted)!="" and str(rpmToBeInserted)!="" and str(airtemp)!="" and str(oiltemp)!="": 
	#if all the data is valid, delete the first entry from rawcodes (-> in rascodes table remains only one entry) and insert the obtained data in processedcodes
	connection.execute("DELETE FROM rawcodes WHERE id IN (SELECT id FROM rawcodes LIMIT 1)");
	connection.execute("INSERT INTO processedcodes(speed, rpm, airtemperature, oiltemperature) VALUES("+str(speedToBeInserted)+", "+str(rpmToBeInserted)+", "+str(airtempToBeInserted)+", "+str(oiltempToBeInserted)+")");
	connection.commit()
   #use fuzzy logic to determine if it was an accident and if so, calculate the priority
speed = ctrl.Antecedent(np.arange(0,255,1), 'speed')
rpm = ctrl.Antecedent(np.arange(0,3500,1), 'rpm')
airtemp = ctrl.Antecedent(np.arange(-40,250,1), 'airtemp')
oiltemp = ctrl.Antecedent(np.arange(-40,250,1), 'oiltemp')
priority = ctrl.Consequent(np.arange(0,3,1), 'priority')

priority.automf(3)
speed.automf(3)
rpm.automf(3)
airtemp.automf(3)
oiltemp.automf(3)

priority['0'] = fuzz.trimf(priority.universe, [0,0,1])
priority['1'] = fuzz.trimf(priority.universe, [0,1,2])
priority['2'] = fuzz.trimf(priority.universe, [1,2,2])

#priority.view()
#airtemp['good']
rule1 = ctrl.Rule((speed['good'] & rpm['good']) | (speed['good'] & rpm['average']) | (speed['average'] & rpm['good']), priority['2'])
rule2 = ctrl.Rule((speed['average'] & rpm['average']) | (speed['average'] & rpm['poor']) | (speed['poor'] & rpm['average']), priority['1'])
rule3 = ctrl.Rule(speed['poor'] & rpm['poor'], priority['0'])

prioritizing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
prioritizing = ctrl.ControlSystemSimulation(prioritizing_ctrl)

#get the two values of the speed from the processedcodes table
cursor1 = connection.execute('SELECT speed FROM processedcodes');
data=[]
for row in cursor1:
    data.append(row[0])
#get the two values of the RPM from the processedcodes table
cursor2 = connection.execute('SELECT rpm FROM processedcodes');
data2=[]
for row in cursor2:
    data2.append(row[0])
    
print("The speeds: " + str(data[0])+" "+str(data[1]));
print("The rpm: " + str(data2[0])+" "+str(data2[1]));

#if the accident was detected, compute the priority
if data[0]>data[1] and data[0]-data[1]>60 and data2[0]>data2[1] and data2[0]-data2[1]>1500:
    prioritizing.input['speed'] = data[0]-data[1]
    prioritizing.input['rpm'] = data2[0]-data2[1]
    prioritizing.compute()
    priorityOfTheAccident = int(round(prioritizing.output['priority']))
    print prioritizing.output['priority']
    print priorityOfTheAccident
   #delete the first entry from processedcodes table -> in the table remains only one entry
    connection.execute("DELETE FROM processedcodes WHERE id IN (SELECT id FROM processedcodes LIMIT 1)");

    GPIO.setmode(GPIO.BOARD)   

    # enable serial communication
    port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1)
	#communicate with the SIM
    port.write('AT'+'\r')
    print port.readline()
    print port.readline()
    port.write('AT+CSQ'+'\r')
    print port.readline()
    print port.readline()
    port.write('AT+CGPSPWR=1'+'\r')
    time.sleep(1)
    print port.readline()
    print port.readline()
	#get the coordinates
    port.write('AT+CGPSINF=0'+'\r')
    print port.readline()
    print port.readline()
    print port.readline()
    s= port.readline()
    data = s.split(",")
    print s
    print port.readline()
    port.write('AT+CMGF=1'+'\r')
    print port.readline()

    port.write('AT+CNMI=2,1,0,0,0'+'\r')  
    print port.readline()
	#send the SMS with the priority, latitude and longitude
    port.write('AT+CMGS="+40741558055"'+'\r')
    time.sleep(1)
    print port.readline()
    time.sleep(1)
    
    port.write(str(priorityOfTheAccident)+" "+str(data[1])+" "+str(data[2])+'\r')  
    time.sleep(1)
    port.write("\x1A") 
    
else:
    print "No accident.."
print ("The sent message: "+str(priorityOfTheAccident)+" "+str(data[1])+" "+str(data[2]))    
connection.close();