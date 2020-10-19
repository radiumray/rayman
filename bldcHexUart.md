```c++


 #include <SimpleFOC.h>

// motor instance
BLDCMotor motor = BLDCMotor(9, 10, 11, 12, 7);



const static uint8_t SPEED_MAX = 20;

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

void setup() {
    motor.voltage_power_supply = 12;
    // limiting motor movements
    motor.voltage_limit = 3;   // rad/s
    motor.velocity_limit = SPEED_MAX; // rad/s
    // open loop control config
    motor.controller = ControlType::velocity_openloop;
    motor.foc_modulation = FOCModulationType::SpaceVectorPWM;
    // init motor hardware
    motor.init();
    Serial.begin(115200);
    Serial.println("Motor ready!");
    _delay(500);


}


float target_velocity = 0;

void loop() {

    motor.move(target_velocity);

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
            // 记录状态值为金庸
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

            target_velocity = (float)pitch;

            Serial.print(yaw);
            Serial.print(",");
            Serial.print(pitch);
            Serial.print(",");
            Serial.println(roll);

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
