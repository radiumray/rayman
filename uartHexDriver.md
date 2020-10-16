

```c++



#define SPEED_MAX 255

#define L_EN 7
#define R_EN 6

#define L_PWM 3
#define R_PWM 2

#define steering_PIN 10

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


/*
 *Mega2560中断通道: 0   1   2   3   4   5
 *Mega2560中断引脚: 2   3   21  20  19  18
*/

const byte interruptPin = 21;

int encoderLeftValue = 0;
unsigned long thisTime, lastTime;


static const uint8_t servoMiddle=90;
static const uint8_t servoRightDegree=50;
static const uint8_t servoLeftDegree=130;

int Ms=500;
int rpm = 0;
const uint8_t rpmMax = 231;

int errorValue = 0;
int powerValue = 0;

//Define Variables we'll be connecting to
double Setpoint, Input, Output;

Servo Steering;

/**
 * 名称：throttle_limit
 * 描述：电机油门控制在一定范围内
 * 输入：PWM
 * 输出：无
 */
int throttle_limit(int pwm){
    int ret=pwm;
    if(ret>SPEED_MAX){
      ret=SPEED_MAX;
    }
    return ret;
}

int potValue = 0;


/**
 * 名称：MotorContrl
 * 描述：电机控制
 * 输入：PWM Dir
 * 输出：无
 */
 void MotorControl(int PWM,int Dir)
 {
    int tempPWM;
    tempPWM=throttle_limit(abs(PWM));
    
    digitalWrite(L_EN,HIGH);
    digitalWrite(R_EN,HIGH);
    switch(Dir)
    {
     case 0: digitalWrite(L_PWM,LOW);
             digitalWrite(R_PWM,LOW);
            // Serial.println("stop");
             break;
     case 1:analogWrite(L_PWM,tempPWM);
            digitalWrite(R_PWM,LOW);
           // Serial.println("go");
            break;
     case 2:digitalWrite(L_PWM,LOW);
            analogWrite(R_PWM,tempPWM);
            //Serial.println("down");
            break;
     default: tempPWM=0; Serial.println("error");;break;
     }
  }

void encoderLeftInterrupt()
{
  encoderLeftValue++;
}

void setup() {

    pinMode(L_EN, OUTPUT);
    pinMode(R_EN, OUTPUT);
    pinMode(L_PWM, OUTPUT);
    pinMode(R_PWM, OUTPUT);

    attachInterrupt(digitalPinToInterrupt(interruptPin), encoderLeftInterrupt, FALLING);

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

            // 不加速度闭环 
            powerValue = abs(speedVal);

            if(speedVal>0) {
              MotorControl(int(powerValue), 2);
            } else if (speedVal<0) {
              MotorControl(int(powerValue), 1);
            } else {
              MotorControl(int(powerValue), 0);
            }

        }
        // 更新上一个byte 
        lastByte = thisByte;
    }


    // thisTime=millis();
    // if(thisTime-lastTime>=Ms) {
    //   rpm=encoderLeftValue;
    //   Input =  map(rpm, 0, rpmMax, 0, 255);
    //   encoderLeftValue=0;
    //   lastTime=thisTime;
    // }


}


```

```py

import serial
import time

dev_fn = '/dev/ttyACM0'
# dev_fn = '/dev/ttyUSB0'
bandRate = 115200

ser = serial.Serial(dev_fn, bandRate, timeout=1)
# ser = serial.Serial(dev_fn, bandRate, timeout=1, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)

angle = 180
threel = 150
ram = 50


def hhh(angle, threel, ram):

    send_list = []
    send_list.append(0xff)
    send_list.append(0xd8)
    send_list.append(angle)
    send_list.append(threel)
    send_list.append(ram)
    send_list.append(0xff)
    send_list.append(0xd9)

    print(send_list)

    # input_s = bytes()
    # print(input_s)
    # num = ser.write(input_s)send_list
    # print(num)
    ser.write(serial.to_bytes(send_list))


for i in range(18):
    hhh(i*10, threel, ram)
    time.sleep(1)


```

