#include <Servo.h>
const static uint8_t motor1B_PIN = 12;
const static uint8_t Servo_PIN = 11;
const static uint8_t motorEN_PIN = 4;

Servo myservo;

void setup() {

  Serial.begin(115200);

  myservo.attach(Servo_PIN);
  delay(200);
  Serial.println("init");


  
  pinMode(motor1B_PIN, OUTPUT);
  digitalWrite(motor1B_PIN, HIGH);

  
  pinMode(motorEN_PIN, OUTPUT);
  digitalWrite(motorEN_PIN, HIGH);
  
}

void loop() {

//  analogWrite(motor1B_PIN,255);
//  Serial.println("motor1B_PIN");
//  
//  delay(3000);



    myservo.write(0);
    Serial.println("0");
    delay(2000);
    myservo.write(90);
    Serial.println("90");
    delay(2000);
    myservo.write(180); 
    Serial.println("180");
    delay(2000);
    myservo.write(90);
    Serial.println("90");
    delay(2000);


}
