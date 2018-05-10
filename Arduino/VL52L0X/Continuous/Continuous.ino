#include <Wire.h>
#include <VL53L0X.h>
#include <Servo.h>

VL53L0X sensor;
Servo servo;

int pos = 0;

void setup()
{
  Serial.begin(9600);
  Wire.begin();
  servo.attach(9);
  sensor.init();
  sensor.setTimeout(500);
  while (!Serial) {
    ;
  }
  sensor.startContinuous();       //time between measurement set by using sensor.startcontiniuos(int)
}

void loop()
{
  for (pos = 0; pos <= 180; pos += 5) {
    servo.write(pos);
    Serial.print(sensor.readRangeContinuousMillimeters()-8);
    Serial.print(" ");
    Serial.print(pos*3.14159/180);
    if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }
    Serial.println();
  }
  for (pos = 180; pos >= 0; pos -= 5) {
    servo.write(pos);
    Serial.print(sensor.readRangeContinuousMillimeters()-45);
    Serial.print(" ");
    Serial.print(pos*3.14159/180);
    if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }
    Serial.println();
  }
}
