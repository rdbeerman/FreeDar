/*
 * Title:         Ultrasonic rangefinger using HC-SR04
 * Author:        R.D. Beerman
 * Date:          18/04/2018
*/
const int trigPin = 9;
const int echoPin = 10;

long duration;
float distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
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
  distance = duration*0.00034/2;
  //send over serial port
  Serial.println(distance);
}
