#include <Wire.h>
#include <VL53L0X.h>
#include <Servo.h>

VL53L0X sensor;
VL53L0X sensor2;
// VL53L0X sensor3;
// VL53L0X sensor4;

int a;
int b;
int c;
int d;

bool detectar = false;

String st1;

int tof(){
a = sensor.readRangeContinuousMillimeters();

  return a;
}

void setup() {
  // Begin the Serial at 9600 Baud
  Serial.begin(115200);
  //Serial1.begin(115200);
  pinMode(13,OUTPUT);
 
////////////////////////////////////////////////////

  // pinMode(7, OUTPUT);
  // pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  // digitalWrite(6, LOW);
  // digitalWrite(7, LOW);

  delay(500);
  Wire.begin();


  //Serial.begin (9600);

  digitalWrite(4, HIGH);
  delay(150);
  //Serial.println("00");
  sensor.init(true);

  //Serial.println("01");
  delay(100);
  sensor.setAddress((uint8_t)01);
//   Serial.println("02");

   digitalWrite(5, HIGH);
     delay(150);
   sensor2.init(true);
//   Serial.println("03");
   delay(100);
   sensor2.setAddress((uint8_t)02);
//   Serial.println("04");
  
//   digitalWrite(6, HIGH);
//   delay(150);
//   sensor3.init(true);
//   Serial.println("05");
//   delay(100);
//   sensor3.setAddress((uint8_t)03);
//   Serial.println("06");
  
//   digitalWrite(7, HIGH);
//   delay(150);
//   Serial.println("07");
//   sensor4.init(true);

//   Serial.println("08");
//   delay(100);
//   sensor4.setAddress((uint8_t)04);
//   Serial.println("09");
//   Serial.println("addresses set");

sensor.startContinuous();
sensor2.startContinuous();
// sensor3.startContinuous();
// sensor4.startContinuous();

/////////////////////////////////////////////////////

}

void loop() {
  if (Serial.available() > 0) {
  st1 = Serial.readStringUntil('\n'); //Read the serial data and store in var
  st1.trim();
  if(st1 == "Seguidor" || st1 == "Obstaculo"){
    detectar = true;
  }
  else{
    detectar = false;
  }
}

while (Serial.available() == 0){
  if (st1 == "Seguidor"){ // Preguntar con los sensores de abajo y medio
    if (detectar){
      if((sensor.readRangeContinuousMillimeters() > 100) && (sensor2.readRangeContinuousMillimeters() > 100)){
        digitalWrite(13,HIGH);
        Serial.write('A');
      }
      if((sensor.readRangeContinuousMillimeters() < 100) && (sensor2.readRangeContinuousMillimeters() < 100)){
        digitalWrite(13,HIGH);
        Serial.write('F');
      }
    }
  }
  if (st1 == "Obstaculo"){ // Preguntar con cualquier sensor
    if (detectar){
      if((sensor.readRangeContinuousMillimeters() > 200) && (sensor2.readRangeContinuousMillimeters() > 200)){
        //digitalWrite(13,HIGH);
        Serial.write('N');  // No detecta
      }
      else if((sensor.readRangeContinuousMillimeters() < 180) && (sensor2.readRangeContinuousMillimeters() < 180)){
        digitalWrite(13,HIGH);
        Serial.write('M');  // Muy lejos
      }
      else if((sensor.readRangeContinuousMillimeters() < 140) && (sensor2.readRangeContinuousMillimeters() < 140)){
        digitalWrite(13,HIGH);
        Serial.write('L');  // Lejos
      }
      else if((sensor.readRangeContinuousMillimeters() < 100) && (sensor2.readRangeContinuousMillimeters() < 100)){
        digitalWrite(13,HIGH);
        Serial.write('S');  // Siempre
      }
      else if((sensor.readRangeContinuousMillimeters() < 80) && (sensor2.readRangeContinuousMillimeters() < 80)){
        digitalWrite(13,HIGH);
        Serial.write('C');  // Cerca
      }
      else if((sensor.readRangeContinuousMillimeters() < 60) && (sensor2.readRangeContinuousMillimeters() < 60)){
        digitalWrite(13,HIGH);
        Serial.write('R');  // Re Cerca
      }
    }
  }
  if (detectar){
    if((sensor.readRangeContinuousMillimeters() > 110) && (sensor2.readRangeContinuousMillimeters() > 110)){
      digitalWrite(13,HIGH);
      Serial.write('A');
      }
    else if((sensor.readRangeContinuousMillimeters() < 50) || (sensor2.readRangeContinuousMillimeters() < 50)){
      digitalWrite(13,LOW);
      Serial.write('C');
      }
    else if((sensor.readRangeContinuousMillimeters() < 70) || (sensor2.readRangeContinuousMillimeters() < 70)){
      digitalWrite(13,LOW);
      Serial.write('M');
      }
    else if((sensor.readRangeContinuousMillimeters() < 100) || (sensor2.readRangeContinuousMillimeters() < 100)){
      digitalWrite(13,LOW);
      Serial.write('L');
      }
    }
  detectar = false;
  break;
  }
}

motoalpinaderrapante
meteelpenederrepente