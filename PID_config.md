


## GBM2804R, AS5048A, SPI, 角度闭环 PID
```c++


motor.PID_velocity.P = 0.08;
motor.PID_velocity.I = 8;
motor.PID_velocity.D = 0;


motor.P_angle.P = 20;
  
  
```
  
  
## GBM2804, AS5600, SPI, 速度闭环 PID
  
```c++
  
pitch_motor.PID_velocity.P = 0.09;
pitch_motor.PID_velocity.I = 8;
pitch_motor.PID_velocity.D = 0.001;
  


## 大疆M2006 P36, SPI, 位置闭环 PID
  
```c++
  motor.PID_velocity.P = 0.065;
  motor.PID_velocity.I = 3;
  motor.PID_velocity.D = 0.0001;
```
