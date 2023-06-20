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
int e;
int f;

bool detectar = false;

String st1;

void setup() {
  // Begin the Serial at 9600 Baud
  Serial.begin(115200);
  pinMode(13,OUTPUT);
 
////////////////////////////////////////////////////

  // pinMode(7, OUTPUT);
  // pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);
  digitalWrite(5, LOW);
  // digitalWrite(6, LOW);
  // digitalWrite(7, LOW);

  delay(500);
  Wire.begin();


  //Serial.begin (9600);

  digitalWrite(2, HIGH);
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
    if (detectar){
      update();
      if (st1 == "Seguidor"){ // Preguntar con los sensores de abajo y medio
        digitalWrite(13,LOW);
        if((a > 100) && (b > 100)){
          Serial.write('A');  // Andar
        }
        if((a < 100) || (b < 100)){
          Serial.write('F');  // Frenar
        }
      }
      if (st1 == "Obstaculo"){ // Preguntar con cualquier sensor
        digitalWrite(13,HIGH);
        if((a > 200) && (b > 200)){
          Serial.write('N');  // No Detecta
        }
        else if((a < 65) || (b < 65)){
          Serial.write('R');  // Re Cerca
        }
        else if((a < 80) && (b < 80)){
          Serial.write('C');  // Cerca
        }
        else if((a < 100) && (b < 100)){
          Serial.write('S');  // Siempre
        }
        else if((a < 140) && (b < 140)){
          Serial.write('L');  // Lejos
        }
        else if((a < 180) && (b < 180)){
          Serial.write('M');  // Muy lejos
        }
      }
    }
    detectar = false;
    break;
  }
}


void update(){
  a = sensor.readRangeContinuousMillimeters() - 10;
  b = sensor2.readRangeContinuousMillimeters() + 10;
  // c = sensor3.readRangeContinuousMillimeters();
  // d = sensor4.readRangeContinuousMillimeters();
  // e = sensor5.readRangeContinuousMillimeters();
  // f = sensor6.readRangeContinuousMillimeters();
}
