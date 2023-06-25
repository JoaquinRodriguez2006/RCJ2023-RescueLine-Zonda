#include <Wire.h>
#include <VL53L0X.h>
#include <Servo.h>

Servo Servin;
Servo Servo;

int t = 30; // Tiempo en milisegundos para los servos

VL53L0X sensor_ru;   // Sensor Right-up
VL53L0X sensor_rd;   // Sensor Right-down
VL53L0X sensor_lu;   // Sensor Left-up
VL53L0X sensor_ld;   // Sensor Left-down

int a;
int b;
int c;
int d;

int pin_ru = 2;
int pin_rd = 3;

int pin_lu = 7;
int pin_ld = 6;

int cont = 0;

bool detectar = false;
bool mov_big_up = false;
bool mov_big_down = false;
bool mov_small_open = false;
bool mov_small_closed = false;

String st1;

void setup() {
  // Begin the Serial at 9600 Baud
  Serial.begin(115200);
  Servin.attach(10);
  Servo.attach(11);
  pinMode(13,OUTPUT);
  
  Servin.write(70);
  Servo.write(160);
 
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

// Pin Right Up
  digitalWrite(pin_ru, HIGH);
  delay(150);
  // Serial.println("00");
  sensor_ru.init(true);

  // Serial.println("01");
  delay(100);
  sensor_ru.setAddress((uint8_t)01);
  // Serial.println("02");

// Pin Right Down
  digitalWrite(pin_rd, HIGH);
  delay(150);
  sensor_rd.init(true);
  // Serial.println("03");
  delay(100);
  sensor_rd.setAddress((uint8_t)02);
  // Serial.println("04");

// Pin Left Down
  digitalWrite(pin_ld, HIGH);
  delay(150);
  sensor_ld.init(true);
  // Serial.println("05");
  delay(100);
  sensor_ld.setAddress((uint8_t)03);
  // Serial.println("06");

// Pin Left Up
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
    if(st1 == "Seguidor" || st1 == "Obstaculo" || st1 == "Rescue"){
      detectar = true;
    }
    else if (st1 == "Mov_Big_Up"){
      mov_big_up = true;
    }
    else if (st1 == "Mov_Big_Down"){
      mov_big_down = true;
    }
    else if (st1 == "Mov_Small_Open"){
      mov_small_open = true;
    }
    else if (st1 == "Mov_Small_Closed"){
      mov_small_closed = true;
    }
    else{
      detectar = false;
      mov_big_up = false;
      mov_big_down = false;
      mov_small_open = false;
      mov_small_closed = false;
    }
  }

  while (Serial.available() == 0){
    if (detectar){
      update();
    }
// LINE - FOLLOWER
      if (st1 == "Seguidor"){ // Preguntar con los sensores de abajo y medio
        digitalWrite(13,LOW);
        if((a > 110) && (b > 110)){
          Serial.write('A');  // Andar
          cont = 0;
        }
        if((a < 110) || (b < 110)){
          // Serial.println(a);
          // Serial.println(b);
          cont = cont+1;
          if (cont > 3){
            Serial.write('F');  // Frenar
            cont = 0;
          }
        }
      }

// RESCUE
  // Explore
      if (st1 == "Rescue"){
        if((a > 200) && (b > 200)){
          Serial.write('u');  // Nule
        }
      else if((a < 80) && (b < 80)){
          Serial.write('n');  // Near
        }
      else if((a < 100) && (b < 100)){
        Serial.write('a');  // Always
      }
      else if((a < 140) && (b < 140)){
        Serial.write('f');  // Far
      }

  // Despositing the cube
      if (st1 == "Rescue_dc"){ // Rescue Cube Down: It is basically an order for the Arduino to deposit the cube
        Deposit_Cube();
        // if Deposit_Cube(){
        //   Serial.write('CONFIRMED');
        // }
        // else{
        //   Serial.write('ERROR OCURRED');
        // }
      }
    
  // Rescuing the Victim
      if (st1 == "Spotted_Victim") {
        Rescuing_Victim();
        // if Rescuing_Victim() {
        //   Serial.write('CONFIRMED');
        // }
        // else{
        //   Serial.write('ERROR OCURRED');
        // }
      }

  // Looking for the victim
      if (st1 == "Rescue_lv") {
        if((c > 200) && (d > 200)){
          Serial.write('U');  // Nule
          }
        else if((c > 80) && (d > 80)){
          Serial.write('N');  // Near
          }
        else if((c > 100) && (d > 100)){
          Serial.write('A');  // Always
          }
        else if((c > 140) && (d > 140)){
          Serial.write('F');  // Far
          
      }        
      
// OBSTACLE
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
    else if (mov_big_up){
      Mov_Servo(t,160);
      // delay(400);
      Serial.write('O');   // OK arriba  
    }
    else if (mov_big_down){
      Mov_Servo(t,30);
      // delay(400);
      Serial.write('O');   // OK abajo
    }
    else if (mov_small_open){
      Mov_Servin(t,10);
      // delay(400);
      Serial.write('O');   // OK abierto
    }
    else if (mov_small_closed){
      Mov_Servin(t,70);
      // delay(400);
      Serial.write('O');   // OK cerrado
    }


    mov_big_up = false;
    mov_big_down = false;
    mov_small_open = false;
    mov_small_closed = false;
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

void Mov_Servo(int tiempo, int destino){ // Movimiento regulado en el tiempo del Servo Grande
  if (Servo.read() > destino){           
    for (int pos = Servo.read(); pos >= destino; pos -= 1) {    // Si la posicion del servo es mayor al de destino va a restar
      Servo.write(pos);          
      delay(tiempo);                     
    }
  }
  else{
    for (int pos = Servo.read(); pos <= destino; pos += 1) {    // Si la posicion del servo es menor al de destino va a sumar
    Servo.write(pos);              
    delay(tiempo);                       
    }
  }
}

void Mov_Servin(int tiempo, int destino){ // Movimiento regulado en el tiempo del Servo Chiquito
  if (Servin.read() > destino){           
    for (int pos = Servin.read(); pos >= destino; pos -= 1) {    // Si la posicion del servo es mayor al de destino va a restar
      Servin.write(pos);          
      delay(tiempo);                     
    }
  }
  else{
    for (int pos = Servin.read(); pos <= destino; pos += 1) {    // Si la posicion del servo es menor al de destino va a sumar
    Servin.write(pos);              
    delay(tiempo);                       
    }
  }
}

void Deposit_Cube(){
  Mov_Servo(t,30);
  Mov_Servin(t,10);
  Mov_Servo(t,160);
  Mov_Servin(t,70);
}

void Rescuing_Victim() {
  Mov_Servo(t,90);
  Mov_Servin(t,10);
  Mov_Servo(t,30);
  Mov_Servin(t,70);
  Mov_Servo(t,160);
}
