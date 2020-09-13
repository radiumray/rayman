```py

odrv0.erase_configuration()


odrv0.config.brake_resistance=0
odrv0.config.dc_bus_undervoltage_trip_level=8
odrv0.config.dc_bus_overvoltage_trip_level=56
odrv0.axis0.motor.config.pole_pairs=7
odrv0.axis0.motor.config.calibration_current=3
odrv0.axis0.motor.config.resistance_calib_max_voltage = 2
odrv0.axis0.motor.config.motor_type=MOTOR_TYPE_HIGH_CURRENT
odrv0.axis0.motor.config.current_lim=20
odrv0.axis0.motor.config.requested_current_range=20



odrv0.axis0.controller.config.vel_gain=0.01
odrv0.axis0.controller.config.vel_integrator_gain=0.05
odrv0.axis0.controller.config.control_mode=CTRL_MODE_VELOCITY_CONTROL
odrv0.axis0.sensorless_estimator.config.pm_flux_linkage=5.51328895422/(7*950)

odrv0.axis0.controller.vel_setpoint=400
odrv0.axis0.motor.config.direction=1


odrv0.axis0.requested_state=AXIS_STATE_MOTOR_CALIBRATION

odrv0.axis0.motor.config.pre_calibrated=True


odrv0.save_configuration()
odrv0.reboot()

odrv0.axis0.controller.vel_setpoint=400
odrv0.axis0.requested_state=AXIS_STATE_SENSORLESS_CONTROL

dump_errors(odrv0)


```
