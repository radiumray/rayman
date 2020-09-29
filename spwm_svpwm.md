```c++


#include "SimpleFOC.h"

BLDCMotor motor = BLDCMotor(9, 10, 11, 7, 8);

void setup() {
    // motor.voltage_power_supply = 12;
    motor.voltage_power_supply = 12;

    // motor.foc_modulation = FOCModulationType::SinePWM; //spwm
    motor.foc_modulation = FOCModulationType::SpaceVectorPWM; //svpwm

    motor.voltage_limit = 6;
    // motor.velocity_limit = 20;

    motor.controller = ControlType::velocity_openloop;

    motor.init();

    Serial.begin(115200);
    Serial.println("Motor ready!");
    _delay(1000);

}

float target_velocity = 1;

void loop() {

    motor.move(target_velocity);

    serialReceiveUserCommand();

}

// utility function enabling serial communication with the user to set the target values
// this function can be implemented in serialEvent function as well
void serialReceiveUserCommand() {
  
  // a string to hold incoming data
  static String received_chars;
  
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the string buffer:
    received_chars += inChar;
    // end of user input
    if (inChar == '\n') {
      
      // change the motor target
      target_velocity = received_chars.toFloat();
      Serial.print("Target velocity ");
      Serial.println(target_velocity);
      
      // reset the command buffer 
      received_chars = "";
    }
  }
}


```
