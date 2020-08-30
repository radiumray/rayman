#include "MsTimer2.h"
// #include "PinChangeInt.h"

int AIN1 = 8;
int AIN2 = 7;
int PWMA = 6;

int SensorINPUTA = 2;      //中断0，也就是数字引脚2---电机A相
int SensorINPUTB = 3;      //电机B相

int PWM_MAX = 255;
float SKp=0.2,SKi=0.4;

int SPWM = 0;
// int target_v = 30;
int target_v = 0;
int encoder_v = 0;
int last_encoder_v = 0;

int sensorPin = A0;
int sensorValue = 0;

void TimerInt(){
  SPWM = Incremental_PI( encoder_v, target_v);
  if(SPWM > PWM_MAX) SPWM = PWM_MAX;
  else if(SPWM < -PWM_MAX) SPWM = -PWM_MAX;
  motor_setPWM(SPWM); 
  last_encoder_v = encoder_v;
  encoder_v = 0;

  // Serial.print("qh-0-");
  Serial.print(last_encoder_v);
  Serial.print(",");
  Serial.print(target_v);
  // Serial.println("-ed");
  Serial.println();
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
  pinMode( AIN1, OUTPUT );                         
  pinMode( AIN2, OUTPUT );
  pinMode( PWMA, OUTPUT ); 
}


void motor_setPWM(int MPWM){
  if (MPWM > 0){   
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);  
  } else{             
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW); 
  }
  analogWrite(PWMA, abs(MPWM));
}

int Incremental_PI (int Encoder,int Target)
{
   static int Bias,Pwm,Last_bias;
   Bias=Encoder-Target;                
   Pwm+=SKp*(Bias-Last_bias)+SKi*Bias;   
   Last_bias=Bias;                     
   return Pwm;                        
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
  sensorValue = analogRead(sensorPin);
  target_v = map(sensorValue, 0, 1023, -110, 110);
  // Serial.println(sensorValue);
}