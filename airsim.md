
## github:
https://github.com/microsoft/AirSim

## 启动命令
```bash
# ubuntu版本
./CityEnviron.sh -ResX=640 -ResY=480 -windowed

# windows版本
CityEnviron.exe -WINDOWED -ResX=640 -ResY=480
```


## airsim settings.json配置

```bash

#存储位置：
# windows：
# C:\Users\24036\Documents\AirSim\settings.json

{
	"SeeDocsAt": "https://github.com/Microsoft/AirSim/blob/master/docs/settings.md",
	"SettingsVersion": 1.2, 
	"SimMode": "Car",
	"LogMessagesVisible": true,

	"CameraDefaults": {
	    "CaptureSettings": [
	      {
	        "ImageType": 0,
	        "Width": 384,
	        "Height": 216,
	        "FOV_Degrees": 90,
	        "AutoExposureSpeed": 100,
	        "AutoExposureBias": 0,
	        "AutoExposureMaxBrightness": 0.64,
	        "AutoExposureMinBrightness": 0.03,
	        "MotionBlurAmount": 0,
	        "TargetGamma": 1.0,
	        "ProjectionMode": "",
	        "OrthoWidth": 5.12
	      }
	    ]

	  },


	//测试目标检测地点
	"Vehicles": {
		"Car1": {
		  "VehicleType": "PhysXCar",
		  "X": 17.24,
		  "Y": -170,
		  "Z": 0,
		  "Pitch": 0, 
		  "Roll": 0, 
		  "Yaw": -90

		}
	}
	
	//测试车道线地点
	"Vehicles": {
	"Car1": {
	  "VehicleType": "PhysXCar",
	  "X": 49.7876,
	  "Y": 207.6644,
	  "Z": 1.3796,
	  "Pitch": 0, 
	  "Roll": 0, 
	  "Yaw": 0
	}

}


```






## 控制脚本
```python


# ready to run example: PythonClient/car/hello_car.py

import airsim
import time
import tempfile
import os
import numpy as np
import cv2


# connect to the AirSim simulator
client = airsim.CarClient(ip="172.32.5.168")
client.confirmConnection()
client.enableApiControl(True)


print("API Control enabled: %s" % client.isApiControlEnabled())
car_controls = airsim.CarControls()

saveDir = os.getcwd()

tmp_dir = os.path.join(saveDir, "airsim_car")
print("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

idx = 0

while True:

    idx=idx+1
    # get state of the car
    car_state = client.getCarState()
    print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))


    # gps_data =  client.getGpsData()
    x = client.simGetVehiclePose().position.x_val
    y = client.simGetVehiclePose().position.y_val
    z = client.simGetVehiclePose().position.z_val
    print('x: {} y: {} z: {}'.format(x, y, z))


    # set the controls for car
    car_controls.throttle = 1
    # car_controls.steering = 1
    client.setCarControls(car_controls)

    # let car drive a bit
    time.sleep(0.1)
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.DepthVis, False, False), # 
        # airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True),
        # airsim.ImageRequest("1", airsim.ImageType.Scene),
        airsim.ImageRequest("1", airsim.ImageType.Scene, False, False),

        ])

    for response_idx, response in enumerate(responses):
        filename = os.path.join(tmp_dir, f"{idx}_{response.image_type}_{response_idx}")

        # 深度图像
        if response.image_type == airsim.ImageType.DepthVis:
            print('compress:', response.compress)
            print('depth:')

            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
            img_gray = img1d.reshape(response.height, response.width, 3)
            print(img1d.shape)
            cv2.imshow('ddd', img_gray)

        # 原始图像
        elif response.image_type == airsim.ImageType.Scene:
            # print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) # get numpy array
            img_rgb = img1d.reshape(response.height, response.width, 3) # reshape array to 3 channel image array H X W X 3
            print(img_rgb.shape)
            # cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb) # write to png
            cv2.imshow('sss', img_rgb)

        else: 
            pass


    key = cv2.waitKey(1)
    if key == 27:
        break


cv2.destroyAllWindows()

#restore to original state
client.reset()

client.enableApiControl(False)



```












参考：

https://blog.csdn.net/MangoHHHH/article/details/107215512

https://microsoft.github.io/AirSim/build_linux/

1. 编译虚幻引擎
```bash


git clone -b 4.24 https://github.com/EpicGames/UnrealEngine

cd UnrealEngine
./Setup.sh
./GenerateProjectFiles.sh
make

```

2. 编译Airsim
```bash

git clone https://github.com/Microsoft/AirSim.git
cd AirSim


执行 ./setup.sh 过程中他会下载一个叫 car_assets.zip 的文件，巨慢，还不一定下载成功！这是一个汽车仿真的模型，如果你想要安装这个，首先要下载 car_assets.zip 文件，文件我下好了放在百度云了
链接：https://pan.baidu.com/s/1zf74BZ1–qSpsltXl8t_SQ 提取码：hss9

下载下来以后放在一个你找得到的地方，然后修改 AirSim 文件夹里的 setup.sh 文件，用文本编辑器打开，在121行左右有一句

wget https://github.com/Microsoft/AirSim/releases/download/v1.2.0/car_assets.zip


将这行改成

cp /home/lizaozao/Desktop/car_assets.zip  car_assets.zip


这里的 /home/lizaozao/Desktop/car_assets.zip 是我文件的存放路径，你要把它改成你的文件所在的路径，修改过后，就可以按照上面给的指令安装了。如果不需要这个汽车，你可以不用修改文件，把

./setup.sh


换成

./setup.sh --no-full-poly-car



./setup.sh
./build.sh
# use ./build.sh --debug to build in debug mode

```



