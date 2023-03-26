/*
  * Original Library soruce: https://github.com/adafruit/Adafruit_VL53L0X
  * 
 * Using 2 VL53L0X Laser Distance Sensors
 * 
 * 
 * Watch video instructions for this code: https://youtu.be/0glBk917HPg
 * 
Updated by Ahmad Shamshiri in April 09, 2021
Custom code for Armin Anzh coment udner this video https://youtu.be/0glBk917HPg
Ahmad from Canada (originally from The Great Khurasan)
 
 * in Ajax, Ontario, Canada. www.robojax.com
 * 
  Need wiring diagram from this code:  https://youtu.be/0glBk917HPg
  Purchase My Arduino course on Udemy.com http://robojax.com/L/?id=62
 * 

 * Get this code and other Arduino codes from Robojax.com


If you found this tutorial helpful, please support me so I can continue creating 
content like this. make donation using PayPal http://robojax.com/L/?id=64

 *  * This code is "AS IS" without warranty or liability. Free to be used as long as you keep this note intact.* 
 * This code has been download from Robojax.com
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
#include "Adafruit_VL53L0X.h"

// address we will assign for all 4 sensor
#define LOX1_ADDRESS 0x30
#define LOX2_ADDRESS 0x31
#define LOX3_ADDRESS 0x32
#define LOX4_ADDRESS 0x33
int sensor1,sensor2, sensor3,sensor4;


// set the pins to shutdown for all 4 sensors
#define SHT_LOX1 2
#define SHT_LOX2 3
#define SHT_LOX3 4
#define SHT_LOX4 5

// objects for the vl53l0x
Adafruit_VL53L0X lox1 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox3 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox4 = Adafruit_VL53L0X();

// this holds the measurement
VL53L0X_RangingMeasurementData_t measure1;
VL53L0X_RangingMeasurementData_t measure2;
VL53L0X_RangingMeasurementData_t measure3;
VL53L0X_RangingMeasurementData_t measure4;

/*
    Reset all sensors by setting all of their XSHUT pins low for delay(10), then set all XSHUT high to bring out of reset
    Keep sensor #1 awake by keeping XSHUT pin high
    Put all other sensors into shutdown by pulling XSHUT pins low
    Initialize sensor #1 with lox.begin(new_i2c_address) Pick any number but 0x29 and it must be under 0x7F. Going with 0x30 to 0x3F is probably OK.
    Keep sensor #1 awake, and now bring sensor #2 out of reset by setting its XSHUT pin high.
    Initialize sensor #2 with lox.begin(new_i2c_address) Pick any number but 0x29 and whatever you set the first sensor to
 */
void setID() {
///Robojax.com code see video https://youtu.be/0glBk917HPg  
  // all reset
  digitalWrite(SHT_LOX1, LOW);    
  digitalWrite(SHT_LOX2, LOW);
  digitalWrite(SHT_LOX3, LOW);    
  digitalWrite(SHT_LOX4, LOW);  
  
  delay(10);
  // all unreset
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, HIGH);
  digitalWrite(SHT_LOX3, HIGH);
  digitalWrite(SHT_LOX4, HIGH);  
  delay(10);

  // activating LOX1 and reseting LOX2
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, LOW);
  digitalWrite(SHT_LOX3, LOW);
  digitalWrite(SHT_LOX4, LOW);

  // initing LOX1
  if(!lox1.begin(LOX1_ADDRESS)) {
    Serial.println(F("Failed to boot first VL53L0X"));
    while(1);
  }
  delay(10);

  ///************************* sensor 2 activation 
  // activating LOX2
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  //initing LOX2
  if(!lox2.begin(LOX2_ADDRESS)) {
    Serial.println(F("Failed to boot second VL53L0X"));
    while(1);
  }
  
   ///************************* sensor3 activation  
  // activating LOX3
  digitalWrite(SHT_LOX3, HIGH);
  delay(10);

  //initing LOX3
  if(!lox3.begin(LOX3_ADDRESS)) {
    Serial.println(F("Failed to boot second VL53L0X"));
    while(1);
  }  
  
  
   ///************************* sensor4 activation  
  // activating LOX4
  digitalWrite(SHT_LOX4, HIGH);
  delay(10);

  //initing LOX4
  if(!lox4.begin(LOX4_ADDRESS)) {
    Serial.println(F("Failed to boot second VL53L0X"));
    while(1);
  }  
    
///Robojax.com code see video https://youtu.be/0glBk917HPg  
}

void read_quad_sensors() {
  
  lox1.rangingTest(&measure1, false); // pass in 'true' to get debug data printout!
  lox2.rangingTest(&measure2, false); // pass in 'true' to get debug data printout!
  lox3.rangingTest(&measure3, false); // pass in 'true' to get debug data printout!
  lox4.rangingTest(&measure4, false); // pass in 'true' to get debug data printout!

  
  // print sensor one reading
  Serial.print("1: ");
  if(measure1.RangeStatus != 4) {     // if not out of range
    sensor1 = measure1.RangeMilliMeter;    
    Serial.print(sensor1);
    Serial.print("mm");    
  } else {
    Serial.print("Out of range");
  }
  
  Serial.print(" ");

  // print sensor two reading
  Serial.print("2: ");
  if(measure2.RangeStatus != 4) {
    sensor2 = measure2.RangeMilliMeter;
    Serial.print(sensor2);
    Serial.print("mm");
  } else {
    Serial.print("Out of range");
  }
 

   Serial.print(" ");

   ///Robojax.com code see video https://youtu.be/0glBk917HPg
  // print sensor three reading
  Serial.print("3: ");
  if(measure3.RangeStatus != 4) {
    sensor3 = measure3.RangeMilliMeter;
    Serial.print(sensor3);
    Serial.print("mm");
  } else {
    Serial.print("Out of range");
  }
  
  
  Serial.print(" ");

  // print sensor four reading
  Serial.print("4: ");
  if(measure4.RangeStatus != 4) {
    sensor4 = measure4.RangeMilliMeter;
    Serial.print(sensor4);
    Serial.print("mm");
  } else {
    Serial.print("Out of range");
  }  
  Serial.println();
}

void setup() {
  ///Robojax.com code see video https://youtu.be/0glBk917HPg
  Serial.begin(115200);

  // wait until serial port opens for native USB devices
  while (! Serial) { delay(1); }

  pinMode(SHT_LOX1, OUTPUT);
  pinMode(SHT_LOX2, OUTPUT);
  pinMode(SHT_LOX3, OUTPUT);
  pinMode(SHT_LOX4, OUTPUT);  

  Serial.println("Shutdown pins inited...");

  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  digitalWrite(SHT_LOX3, LOW);
  digitalWrite(SHT_LOX4, LOW);

  Serial.println("All four in reset mode...(pins are low)");
  
  
  Serial.println("Starting...");
  setID();
 
}

void loop() {
   
  read_quad_sensors();//robojax.com code
  delay(100);
}
