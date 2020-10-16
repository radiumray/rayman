```c++

#include "SimpleFOC.h"

// motor instance
BLDCMotor motor = BLDCMotor(9, 10, 11, 7, 7);

float target_position = 0; // rad/s
float angle_wheel = 0; // rad/s
float radian = 0.0;

int value = 0 ;


void setup() {
	// power supply voltage
	// default 12V
	motor.voltage_power_supply = 12;

	// limiting motor movements
	motor.voltage_limit = 3;   // rad/s
	motor.velocity_limit = 20; // rad/s
	// open loop control config
	motor.controller = ControlType::angle_openloop;
	motor.foc_modulation = FOCModulationType::SpaceVectorPWM;

	// init motor hardware
	motor.init();

	Serial.begin(115200);
	Serial.println("Motor ready!");

	_delay(500);
	value = pulseIn(2, HIGH);
	radian = TWO_PI*value/1023;
	target_position = radian;
	motor.move(target_position);
	
}



void loop() {

	value = pulseIn(2, HIGH);
	Serial.print(value);
	Serial.print(" ");

	float filterValue = motor.rayFilter(value, motor.LPF_velocity);
	Serial.println(filterValue);

	radian = TWO_PI*filterValue/1023;

	target_position = radian;
	//  Serial.println(radian);

	motor.move(target_position + angle_wheel);
	serialReceiveUserCommand();

}

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
      angle_wheel = received_chars.toFloat();
    //   Serial.print("Target position: ");
    //   Serial.println(angle_wheel);
      
      // reset the command buffer 
      received_chars = "";
    }
  }
}



```
