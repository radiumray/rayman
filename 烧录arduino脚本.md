```bash



echo "***************************"
echo "burn arduino hex"
echo "***************************"

/snap/arduino/61/hardware/tools/avr/bin/avrdude -C/snap/arduino/61/hardware/tools/avr/etc/avrdude.conf -v -patmega2560 -cwiring -P/dev/ttyACM0 -b115200 -D -Uflash:w:/home/lamb/init_scripts/mecnumMotorROSCAN.ino.hex:i 

echo "***************************"
echo "del arduino hex"
echo "***************************"

cd /home/lamb/init_scripts/
pwd
rm mecnumMotorROSCAN.ino.hex

echo "***************************"
echo "init AP scripts"
echo "***************************"

sh system_init.sh


```
