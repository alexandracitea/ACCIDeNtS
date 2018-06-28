#include <SoftwareSerial.h>
               
String Grsp;
SoftwareSerial gsm(6,7); // RX, TX
String phoneNumber = "+40741558055";

void setup() { //conenct to the SIM
  Serial.begin(9600);
  gsm.begin(9600);
  gsm.println("ATE0");
  gsm.println("AT");
  gsm.println("AT+CMGF=1");
  gsm.println("AT+CNMI=1,2,0,0,0");
}

void loop() { //listen for SMSs, when received print to serial the data including priority and coordinates
  if(gsm.available()) {
    Grsp = gsm.readString();
    if( Grsp.substring(9,21).equals(phoneNumber)){ //check phone number
      Serial.println(Grsp.substring(48));
    }
}
}
