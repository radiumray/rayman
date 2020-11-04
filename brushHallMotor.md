```c++


/*
 *Mega2560中断通道: 0   1   2   3   4   5
 *Mega2560中断引脚: 2   3   21  20  19  18
*/

#include "MsTimer2.h"
#define SPEED_MAX 255

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


#define steering_PIN 6
#include <Servo.h>


// 定义协议包的长度
const static uint8_t dataHexLen=8;
// 定义帧头, 帧尾 借鉴 jpg压缩
const static byte frameHexH = 0xff;
const static byte frameHead = 0xd8;

const static byte frameHexT = 0xd9;
const static byte frameTail = 0x00;

// 存储Hex指令包
char dataCommand[dataHexLen];
// 是否存储hex指令状态值
bool isStart = false;
// 记录前一个byte
byte lastByte = 0x00;
// 记录当前byte
byte thisByte = 0x00;
// 指令包位置索引
uint8_t index = 0;

// int powerValue = 0;

static const uint8_t servoMiddle=90;
static const uint8_t servoRightDegree=50;
static const uint8_t servoLeftDegree=130;

Servo Steering;

int throttle_limit(int pwm){
    int ret=pwm;
    if(ret > SPEED_MAX){
      ret = SPEED_MAX;
    }
    return ret;
}


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

void setup() {

    motor_init();
    pinMode(SensorINPUTA, INPUT_PULLUP);        
    pinMode(SensorINPUTB, INPUT_PULLUP);        

    //下降沿触发，触发中断0，调用exti_moter1函数
    attachInterrupt(0, exti_moter1, RISING);
    MsTimer2::set(100, TimerInt);
    MsTimer2::start();

    Steering.attach(steering_PIN);
    Steering.write(servoMiddle);

    Serial.begin(115200);
}

void loop() {

    while(Serial.available()) {
        // 读取当前byte
        byte incomingByte = Serial.read();

        // Serial.print(char(incomingByte));

        // 赋值当天byte给thisByte
        thisByte = incomingByte;

        // 如果遇到接收到的两个相邻的bytes是帧头FF D8, 则开始存储指令
        if (lastByte == frameHexH && thisByte == frameHead) {
            // 启动开始记录状态
            isStart=true;
            // 位置索引为0
            index=0;
            // 赋值帧头
            dataCommand[index++]=char(lastByte);
            dataCommand[index]=char(thisByte);
        }

        // 如果存储状态为启动, 则追加hex命令
        if (isStart) {
            dataCommand[index++]=char(thisByte);
        }

        // 如果遇到帧尾, 则停止记录并输出显示
        if (lastByte == frameHexT && thisByte == frameTail) {
            // 记录状态值为金庸
            isStart=false;
            // 追加hex指令
            dataCommand[index++]=char(thisByte);
            // 初始化位置索引为0
            index=0;

            // Serial.println(dataCommand);

            // 转换, 打印指令值 
            uint8_t angle = (uint8_t)dataCommand[2];
            uint8_t three = (uint8_t)dataCommand[3];
            uint8_t ramba = (uint8_t)dataCommand[4];
            // Serial.print(angle);
            // Serial.print(",");
            // Serial.print(three);
            // Serial.print(",");
            // Serial.println(ramba);

            // 方向控制
            uint8_t servoVal = map(angle, 0, 255, servoLeftDegree, servoRightDegree);
            Steering.write(servoVal);

            // 速度控制
            int16_t speedVal = map(three, 0, 255, -255, 255);
            motor_setPWM(speedVal);

        }
        // 更新上一个byte 
        lastByte = thisByte;
    }

}


```
