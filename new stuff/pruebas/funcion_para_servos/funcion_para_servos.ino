#include <Servo.h>

Servo Servin;
Servo Servo;

int t = 15; // Tiempo en milisegundos para los servos

void setup() {
  // put your setup code here, to run once:
  Servin.attach(10);
  Servo.attach(11);
  Servin.write(70);
}

void loop() {

  // Aca va el movimiento de los servos
  Mov_Servo(t,160);
  Mov_Servo(t,30);

  Mov_Servin(t,10);
  Mov_Servin(t,70);

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
