/*
 * Title:         Ultrasonic rangefinger using HC-SR04
 * Author:        R.D. Beerman
 * Date:          18/04/2018
*/
#include <Servo.h>;
#include <Wire.h>;
Servo servo;

#define echoPin 2 
#define trigPin 3 

int pos = 0;

long duration;
float distance;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  servo.attach(9);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  for (pos = 0; pos <= 180; pos += 5) {
    servo.write(pos);
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin,HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = duration*0.34/2;
    Serial.print(distance);
    Serial.print(" ");
    Serial.print(pos*3.14159/180);
    Serial.println();
    //delay(50);      // calm down
  }
 for (pos = 180; pos >= 0; pos -= 5) {
    servo.write(pos);
    // clear trigpin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // start measurement
    digitalWrite(trigPin,HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // read result
    duration = pulseIn(echoPin, HIGH);
    // calc distance
    distance = duration*0.34/2;
    //send over serial port
    Serial.print(distance);
    Serial.print(" ");
    Serial.print(pos*3.14159/180);
    Serial.println();
    //delay(50);    //calm down
  }
}
