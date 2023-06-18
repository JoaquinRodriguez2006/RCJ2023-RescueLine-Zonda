#include <Servo.h>

Servo Servin;
Servo Servo;
int velocity = 60;

void setup() {
  // put your setup code here, to run once:
  Servin.attach(10);
  Servo.attach(11);
}

void loop() {
  // put your main code here, to run repeatedly:
  Servo.write(map(60, -100, 100, 0, 180));
  delay(1000);
  Servo.write(map(70, -100, 100, 0, 180));
  delay(1000);

  // Servin.write(90);
  // delay(1000);
  // Servo.write(160); 
  // delay(1000);
  // Servo.write(85); 
  // delay(1000);
  // Servin.write(10);
  // delay(1000);
  // Servin.write(90);
  // delay(1000);

  // Servo.write(100); // Pone arriba el servo grande
  // delay(1000);
  // Servin.write(90); // Cierra servo chiquito
  // delay(1000);
  // Servin.write(13);  // Pone casi abajo el servo grande
  // delay(1000);
  // Servo.write(30);  // Abre servo chiquito
  // delay(1000);
  // Servin.write(90);   // Pone abajo el servo grande
  // delay(1000);
  // Servo.write(90);  // Abre servo chiquito
  // delay(1000);
  // Servo.write(160);  // Abre servo chiquito
  // delay(1000);
}