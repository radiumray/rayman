```c++

#include <SimpleFOC.h>

// motor instance
BLDCMotor motor = BLDCMotor(9, 10, 11, 7, 7);

void setup() {
  // power supply voltage
  // default 12V
  motor.voltage_power_supply = 12;

  // limiting motor movements
  motor.voltage_limit = 3;   // rad/s
  motor.velocity_limit = 20; // rad/s
  // open loop control config
  motor.controller = ControlType::angle_openloop;

  // init motor hardware
  motor.init();
  

  Serial.begin(115200);
  Serial.println("Motor ready!");
  _delay(1000);
}

float target_position = 0; // rad/s

void loop() {
  int value = pulseIn(2, HIGH);
  Serial.println(value);
//  Serial.print(" ");

  float radian = TWO_PI*value/1023;
  target_position = radian;
//  Serial.println(radian);

  motor.move(target_position);

}



```
