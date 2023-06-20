#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor_ru;
VL53L0X sensor_rd;
VL53L0X sensor_lu;
VL53L0X sensor_ld;

int a;
int b;
int c;
int d;

int PIN_1 = 4;
int PIN_2 = 5;

int pin_ru = 2;
int pin_rd = 3;

int pin_lu = 7;
int pin_ld = 6;

void setup() {
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
  Serial.begin (9600);

  digitalWrite(pin_ru, HIGH);
  delay(150);
  Serial.println("00");
  sensor_ru.init(true);

  Serial.println("01");
  delay(100);
  sensor_ru.setAddress((uint8_t)01);
  Serial.println("02");

  digitalWrite(pin_rd, HIGH);
  delay(150);
  sensor_rd.init(true);
  Serial.println("03");
  delay(100);
  sensor_rd.setAddress((uint8_t)02);
  Serial.println("04");

  digitalWrite(pin_ld, HIGH);
  delay(150);
  sensor_ld.init(true);
  Serial.println("05");
  delay(100);
  sensor_ld.setAddress((uint8_t)03);
  Serial.println("06");

  digitalWrite(pin_lu, HIGH);
  delay(150);
  Serial.println("07");
  sensor_lu.init(true);

  Serial.println("08");
  delay(100);
  sensor_lu.setAddress((uint8_t)04);
  Serial.println("09");

  sensor_ru.startContinuous();
  sensor_rd.startContinuous();
  sensor_ld.startContinuous();
  sensor_lu.startContinuous();

}

void loop() {
  a = sensor_ru.readRangeContinuousMillimeters();
  Serial.print("RU: ");
  Serial.print(a);
  Serial.print("    ");
  b = sensor_rd.readRangeContinuousMillimeters();
  Serial.print("RD: ");
  Serial.print(b);
  Serial.print("    ");
  c = sensor_ld.readRangeContinuousMillimeters();
  Serial.print("LD: ");
  Serial.print(c);
  Serial.print("    ");
  d = sensor_lu.readRangeContinuousMillimeters();
  Serial.print("LU: ");
  Serial.println(d);

  delay(10);


}
