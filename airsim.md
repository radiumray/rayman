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




./CityEnviron.sh -ResX=640 -ResY=480 -windowed




```bash
./CityEnviron.sh -ResX=640 -ResY=480 -windowed

Airsim.exe -WINDOWED -ResX=640 -ResY=480
```


```python


import airsim
import time
import tempfile
import os
import numpy as np
import cv2


# connect to the AirSim simulator
client = airsim.CarClient()
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

    # set the controls for car
    car_controls.throttle = 1
    car_controls.steering = 1
    client.setCarControls(car_controls)

    # let car drive a bit
    time.sleep(0.1)
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.DepthVis), # 
        # airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True),
        # airsim.ImageRequest("1", airsim.ImageType.Scene),
        airsim.ImageRequest("1", airsim.ImageType.Scene, False, False),

        ])

    for response_idx, response in enumerate(responses):
        filename = os.path.join(tmp_dir, f"{idx}_{response.image_type}_{response_idx}")

        # 深度图像
        if response.image_type == airsim.ImageType.DepthVis:
            print('depth:')
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
            print(img1d.shape)

        # 原始图像
        elif response.image_type == airsim.ImageType.Scene:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
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
