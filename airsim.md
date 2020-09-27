

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
