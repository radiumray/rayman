```c++

#include "MsTimer2.h"

#define L_PWM 3
#define R_PWM 5
#define EN_MOTOR 8

int SensorINPUTA = A2;      //中断0，也就是数字引脚2---电机A相
int SensorINPUTB = 2;      //电机B相

int PWM_MAX = 255;
float SKp=0.5,SKi=0.6;  

int SPWM = 0;
int target_v = 0;
int encoder_v = 0;
int last_encoder_v = 0;

int star_num = 0;


void TimerInt(){
  SPWM = Incremental_PI( encoder_v, target_v);
  if(SPWM > PWM_MAX) SPWM = PWM_MAX;
  else if(SPWM < -PWM_MAX) SPWM = -PWM_MAX;
  motor_setPWM(SPWM); 
  last_encoder_v = encoder_v;
  encoder_v = 0;

  // Serial.print("qh-0-");
  Serial.print(last_encoder_v);
  Serial.print(" ");
  Serial.print(target_v);
  Serial.println();
}


void setup(){
  Serial.begin(115200);
  motor_init();
  pinMode(SensorINPUTA, INPUT_PULLUP);        
  pinMode(SensorINPUTB, INPUT_PULLUP);        

  //下降沿触发，触发中断0，调用exti_moter1函数
  attachInterrupt(0, exti_moter1, RISING);
  MsTimer2::set(100, TimerInt);
  MsTimer2::start();

  
}

void loop() { 
  serialReceiveUserCommand();
}

void exti_moter1(void)
{       
  if(digitalRead(SensorINPUTB) == 1){
    encoder_v++;
  }else{
    encoder_v--;
  }
}

void motor_init(){
  pinMode(L_PWM, OUTPUT);
  pinMode(R_PWM, OUTPUT);
  digitalWrite(L_PWM,LOW);
  digitalWrite(R_PWM,LOW);
  pinMode(EN_MOTOR, OUTPUT);
  digitalWrite(EN_MOTOR,HIGH);
}

int throttle_limit(int pwm){
    int ret=pwm;
    if(ret > PWM_MAX) {
      ret = PWM_MAX;
    }
    return ret;
}


void motor_setPWM(int MPWM){
  uint8_t tempPWM;
  tempPWM=throttle_limit(abs(MPWM));

  if (MPWM > 0){   
    digitalWrite(EN_MOTOR,HIGH);
    analogWrite(L_PWM, tempPWM);
    digitalWrite(R_PWM, LOW);
  } else if (MPWM < 0) { 
    digitalWrite(EN_MOTOR,HIGH);            
    digitalWrite(L_PWM, LOW);
    analogWrite(R_PWM, tempPWM);
  } else {
    digitalWrite(EN_MOTOR,LOW);
    digitalWrite(R_PWM, LOW);
    digitalWrite(L_PWM, LOW);
  }
}

int Incremental_PI (int Encoder,int Target)
{   
   static int Bias,Pwm,Last_bias;
   Bias=Encoder-Target;                
   Pwm+=SKp*(Bias-Last_bias)+SKi*Bias;   
   Last_bias=Bias;                     
   return Pwm;                        
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
      target_v = received_chars.toInt();
      Serial.print("target_v ");
      Serial.println(target_v);
      
      // reset the command buffer 
      received_chars = "";
    }
  }
}


```
