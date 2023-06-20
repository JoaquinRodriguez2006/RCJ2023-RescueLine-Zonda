#include <Wire.h>
#include <VL53L0X.h>
#include <Servo.h>

VL53L0X sensor_ru;
VL53L0X sensor_rd;
VL53L0X sensor_lu;
VL53L0X sensor_ld;

int a;
int b;
int c;
int d;

bool detectar = false;

int pin_ru = 2;
int pin_rd = 3;

int pin_lu = 7;
int pin_ld = 6;

String st1;

void setup() {
  // Begin the Serial at 9600 Baud
  Serial.begin(115200);
  pinMode(13,OUTPUT);
 
////////////////////////////////////////////////////

 pinMode(pin_lu, OUTPUT);
  pinMode(pin_ld, OUTPUT);
  pinMode(pin_rd, OUTPUT);
  pinMode(pin_ru, OUTPUT);
  digitalWrite(pin_ru, LOW);
  digitalWrite(pin_rd, LOW);
  digitalWrite(pin_ld, LOW);
  digitalWrite(pin_lu, LOW);

  delay(500);
  Wire.begin();
  // Serial.begin (9600);

  digitalWrite(pin_ru, HIGH);
  delay(150);
  // Serial.println("00");
  sensor_ru.init(true);

  // Serial.println("01");
  delay(100);
  sensor_ru.setAddress((uint8_t)01);
  // Serial.println("02");

  digitalWrite(pin_rd, HIGH);
  delay(150);
  sensor_rd.init(true);
  // Serial.println("03");
  delay(100);
  sensor_rd.setAddress((uint8_t)02);
  // Serial.println("04");

  digitalWrite(pin_ld, HIGH);
  delay(150);
  sensor_ld.init(true);
  // Serial.println("05");
  delay(100);
  sensor_ld.setAddress((uint8_t)03);
  // Serial.println("06");

  digitalWrite(pin_lu, HIGH);
  delay(150);
  // Serial.println("07");
  sensor_lu.init(true);

  // Serial.println("08");
  delay(100);
  sensor_lu.setAddress((uint8_t)04);
  // Serial.println("09");

  sensor_ru.startContinuous();
  sensor_rd.startContinuous();
  sensor_ld.startContinuous();
  sensor_lu.startContinuous();

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
  a = sensor_ru.readRangeContinuousMillimeters();
  b = sensor_lu.readRangeContinuousMillimeters();
  c = sensor_rd.readRangeContinuousMillimeters();
  d = sensor_ld.readRangeContinuousMillimeters();
  
}
