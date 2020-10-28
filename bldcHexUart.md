```c++


#include "SimpleFOC.h"

#define YAW_MOTOR
#define PITCH_MOTOR

// motor instance
#ifdef YAW_MOTOR
BLDCMotor yaw_motor = BLDCMotor(9, 10, 11, 7, 7);
#endif


#ifdef PITCH_MOTOR
BLDCMotor pitch_motor = BLDCMotor(3, 5, 6, 7, 8);
MagneticSensorI2C sensor = MagneticSensorI2C(0x36, 12, 0x0E, 4);
#endif

const static uint8_t SPEED_MAX = 20;
const static float POSITION_MAX = 0.25;
const static uint8_t VOLTAGE_LIMIT = 3;


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

float target_velocity = 0;
float target_position = 0;
float angle_wheel = 0;
float radian = 0;
int value = 0;


void setup() {

#ifdef YAW_MOTOR   

    yaw_motor.voltage_power_supply = 12;
    // limiting motor movements
    yaw_motor.voltage_limit = VOLTAGE_LIMIT;   // rad/s
    yaw_motor.velocity_limit = SPEED_MAX; // rad/s
    // open loop control config
    yaw_motor.controller = ControlType::angle_openloop;
    yaw_motor.foc_modulation = FOCModulationType::SpaceVectorPWM;
    // init motor hardware
    yaw_motor.init();

#endif

#ifdef PITCH_MOTOR

    sensor.init();
	// link the motor to the sensor
	pitch_motor.linkSensor(&sensor);

    pitch_motor.voltage_power_supply = 12;
    // limiting motor movements
    pitch_motor.voltage_limit = VOLTAGE_LIMIT;   // rad/s
    pitch_motor.velocity_limit = SPEED_MAX; // rad/s
    // open loop control config
    // pitch_motor.controller = ControlType::velocity_openloop;
    pitch_motor.controller = ControlType::velocity;
    pitch_motor.foc_modulation = FOCModulationType::SpaceVectorPWM;

	// pitch_motor.PID_velocity.P = 0.20;
	// pitch_motor.PID_velocity.I = 20;
	// pitch_motor.PID_velocity.D = 0.001;

	pitch_motor.PID_velocity.P = 0.09;
	pitch_motor.PID_velocity.I = 8;
	pitch_motor.PID_velocity.D = 0.001;

	// jerk control using voltage voltage ramp
	// default value is 300 volts per sec  ~ 0.3V per millisecond
	pitch_motor.PID_velocity.output_ramp = 1000;

	// velocity low pass filtering
	// default 5ms - try different values to see what is the best. 
	// the lower the less filtered
	pitch_motor.LPF_velocity.Tf = 0.01;

    // init motor hardware
    pitch_motor.init();

    pitch_motor.initFOC();

#endif

    Serial.begin(115200);
    Serial.println("Motor ready!");
    // _delay(20);

#ifdef YAW_MOTOR
    value = pulseIn(2, HIGH);
    radian = TWO_PI*value/1023;

    // if (radian < -POSITION_MAX) {
    //     radian = - POSITION_MAX;
    // } else if (radian > POSITION_MAX) {
    //     radian = POSITION_MAX;
    // }
    target_position = radian;
    yaw_motor.move(target_position);
#endif

}


void loop() {

#ifdef YAW_MOTOR
    value = pulseIn(2, HIGH);
    float filterValue = yaw_motor.rayFilter(value, yaw_motor.LPF_velocity);
    radian = TWO_PI*filterValue/1023;
    // if (radian < -POSITION_MAX) {
    //     radian = - POSITION_MAX;
    // } else if (radian > POSITION_MAX) {
    //     radian = POSITION_MAX;
    // }
    target_position = radian;
    yaw_motor.move(target_position + angle_wheel);
#endif

#ifdef PITCH_MOTOR 
    pitch_motor.loopFOC();
    pitch_motor.move(target_velocity);
#endif

    receiveUserCommand();
}


void receiveUserCommand() {

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
            // 记录状态值为否
            isStart=false;
            // 追加hex指令
            dataCommand[index++]=char(thisByte);
            // 初始化位置索引为0
            index=0;

            // Serial.println(dataCommand);

            // 转换, 打印指令值 
            uint8_t yaw = (uint8_t)dataCommand[2]; // 方向
            uint8_t pitch = (uint8_t)dataCommand[3]; // 油门
            uint8_t roll = (uint8_t)dataCommand[4]; // 横移


            target_velocity = (float)(pitch-127)/127*SPEED_MAX;

            angle_wheel = (float)(yaw-127)/127*POSITION_MAX;

            // target_velocity = (float)pitch;

            // Serial.print(yaw);
            // Serial.print(",");
            // Serial.print(pitch);
            // Serial.print(",");
            // Serial.println(roll);
            // Serial.println(angle_wheel);

        }
        // 更新上一个byte 
        lastByte = thisByte;
    }
}

```



```py

import serial
import time

# dev_fn = '/dev/ttyACM0'
dev_fn = '/dev/ttyUSB0'
bandRate = 115200

ser = serial.Serial(dev_fn, bandRate, timeout=1)
# ser = serial.Serial(dev_fn, bandRate, timeout=1, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)

angle = 180
threel = 10
ram = 50


def hhh(angle, threel, ram):

    send_list = []
    send_list.append(0xff)
    send_list.append(0xd8)
    send_list.append(angle)
    send_list.append(threel)
    send_list.append(ram)
    send_list.append(0xd9)
    send_list.append(0x00)

    print(send_list)

    # input_s = bytes()
    # print(input_s)
    # num = ser.write(input_s)send_list
    # print(num)
    ser.write(serial.to_bytes(send_list))


for i in range(2):
    hhh(0, 0, 0)
    time.sleep(1)

hhh(0, threel, ram)

```
