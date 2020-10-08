// Open loop motor control example 
#include "SimpleFOC.h"

const static uint8_t voltage_power_supply = 12;
const static uint8_t voltage_limit = 6;
// const static uint8_t voltage_power_supply = 6;
// const static uint8_t voltage_limit = 2;


const static uint8_t velocity_limit = 20;

const static uint8_t motor0_pin_A = 3;
const static uint8_t motor0_pin_B = 5;
const static uint8_t motor0_pin_C = 6;

const static uint8_t motor1_pin_A = 9;
const static uint8_t motor1_pin_B = 10;
const static uint8_t motor1_pin_C = 11;

const static uint8_t motor1_pole_pair = 7;
const static uint8_t motor0_pole_pair = 11;

const static uint8_t potentiometer_pin = A0;


// motor instance
BLDCMotor motor0 = BLDCMotor(motor0_pin_A, 
							motor0_pin_B, 
							motor0_pin_C, 
							motor0_pole_pair);

BLDCMotor motor1 = BLDCMotor(motor1_pin_A, 
							motor1_pin_B, 
							motor1_pin_C, 
							motor1_pole_pair);

MagneticSensorI2C sensor = MagneticSensorI2C(0x36, 12, 0x0E, 4);


void setup() {

	pinMode(potentiometer_pin,INPUT);
  
	// initialise magnetic sensor hardware
	sensor.init();
	// link the motor to the sensor
	motor1.linkSensor(&sensor);

	// power supply voltage
	// default 12V
	motor0.voltage_power_supply = voltage_power_supply;
	motor1.voltage_power_supply = voltage_power_supply;

	// limiting motor movements
	motor0.voltage_limit = voltage_limit;   // rad/s
	motor0.velocity_limit = velocity_limit; // rad/s

	motor1.voltage_limit = voltage_limit;   // rad/s
	motor1.velocity_limit = velocity_limit; // rad/s

	// open loop control config
	// motor.controller = ControlType::velocity_openloop;
	// motor.controller = ControlType::angle_openloop;
	motor0.controller = ControlType::angle_openloop;
	motor1.controller = ControlType::velocity;
	// motor.controller = ControlType::angle;

	// motor.foc_modulation = FOCModulationType::SinePWM;
	motor0.foc_modulation = FOCModulationType::SpaceVectorPWM;
	motor1.foc_modulation = FOCModulationType::SpaceVectorPWM;

	motor1.PID_velocity.P = 0.1;
	motor1.PID_velocity.I = 2.5;
	motor1.PID_velocity.D = 0;

	// jerk control using voltage voltage ramp
	// default value is 300 volts per sec  ~ 0.3V per millisecond
	motor1.PID_velocity.output_ramp = 1000;

	// velocity low pass filtering
	// default 5ms - try different values to see what is the best. 
	// the lower the less filtered
	motor1.LPF_velocity.Tf = 0.01;

	// angle P controller 
	// motor.P_angle.P = 10;

	// init motor hardware
	motor0.init();
	motor1.init();

	// align sensor and start FOC
	motor1.initFOC();

	Serial.begin(115200);
	Serial.println("Motor ready!");
	_delay(1000);
}

float target_value = 0; // rad/s

void loop() {
	// open loop velocity movement 
	// using motor.voltage_limit and motor.velocity_limit
	uint16_t sensorValue = analogRead(A0);
	sensorValue = map(sensorValue, 0, 1023, 0, velocity_limit);
	target_value = (float)sensorValue;

	// main FOC algorithm function
	// the faster you run this function the better
	// Arduino UNO loop  ~1kHz
	// Bluepill loop ~10kHz 
	motor1.loopFOC();

	motor0.move(target_value);
	motor1.move(target_value);

}





/*
// Open loop motor control example 
#include "SimpleFOC.h"

// motor instance
BLDCMotor motor = BLDCMotor(3, 5, 6, 11);

void setup() {
  
  // power supply voltage
  // default 12V
  motor.voltage_power_supply = 12;

  // limiting motor movements
  motor.voltage_limit = 3;   // rad/s
  motor.velocity_limit = 20; // rad/s

  // open loop control config
  motor.controller = ControlType::velocity_openloop;

  // init motor hardware
  motor.init();
  
  Serial.begin(115200);
  Serial.println("Motor ready!");
  _delay(1000);
}

float target_velocity = 0; // rad/s

void loop() {
  // open loop velocity movement 
  // using motor.voltage_limit and motor.velocity_limit
  motor.move(target_velocity);

  // receive the used commands from serial
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

*/
