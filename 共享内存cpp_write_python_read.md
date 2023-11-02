# cpp write:

```c++

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <vector>
#include <string>
 
#define IMAGE_SIZE 480*640*3 //图片大小
using namespace std;
using namespace cv;
 
typedef struct _BOX {
	int  flag;
	char ch[IMAGE_SIZE];//之前用了cv::Mat不行，因为无法在结构体里初始化大小
}Box;
 
int main() {
	int shmid = shmget((key_t)1275, sizeof(Box), 0666|IPC_CREAT);
	void *shm = shmat(shmid, (void*)0, 0);
	Box *pBox = (Box*)shm;
	pBox->flag = 0;
 

   VideoCapture cap(0);

    if(!cap.isOpened()) {
        std::cout << "Error: Failed to access the camera." << std::endl;
        return -1;
    }


	int i = 0;
	while(true)
	{

		// while(pBox->flag == 0)
		// {


			// getchar();

                        // Mat Img=imread("sss.jpg",IMREAD_COLOR);

                        Mat Img;
                        cap >> Img;

                        imshow("write show", Img);


                        std::cerr << "width::" <<  Img.cols << std::endl;
                        std::cerr << "height::" <<  Img.rows << std::endl;
                        std::cerr << "channels::" <<  Img.channels() << std::endl;


                        int size = Img.cols * Img.rows * Img.channels();
                        
                        printf("Memory attached at %p\n", (int *)(shm));

                        std::cerr << "size::" <<  size << std::endl;
                       
                        char *from = (char*)Img.data;

                        memcpy(pBox->ch, from, size);

                        int key = waitKey(30);

                        if (key == 'q') {
                            break;
                        }



		// 	pBox->flag = 0;
		// }
	}
	
	shmdt(shm);
	return 0;
}

```

# python read:

```python

import sysv_ipc
import numpy as np
import cv2

# 设置共享内存的键，确保与C++中使用的键相匹配
key = 1275

# 连接到共享内存
try:
    shm = sysv_ipc.SharedMemory(key)
except sysv_ipc.ExistentialError:
    print("共享内存不存在，请确保先运行C++代码创建共享内存。")
    exit(1)


while True:
    # 读取共享内存中的数据
    shm_data = shm.read()
    # 显示共享内存中的数据

    # print(shm_data.decode("utf-8"))  # 假设数据是UTF-8编码的文本
    # print(len(shm_data[4:]))
    # 将数据解码为NumPy数组
    image_data = np.frombuffer(shm_data[4:], dtype=np.uint8)
    image_data = image_data.reshape((480, 640, 3))

    # 显示图像
    cv2.imshow("Shared Memory Image", image_data)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

# 断开与共享内存的连接
shm.detach()

```

# cpp read:

```c++

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
 

#define IMAGE_SIZE 640*480*3 //图片大小
using namespace std;
 
 
typedef struct _BOX
{
	int  flag;
	char ch[IMAGE_SIZE];
}Box;

int main()
{
	int shmid = shmget((key_t)1275, sizeof(Box), 0666|IPC_CREAT);
	void *shm = shmat(shmid, (void*)0, 0);
	Box *pBox = (Box*)shm;
         size_t sizeofbuf;

	while(1)
	{
		// if(pBox->flag == 1)
		// {
			
                        cv::Mat cvoutImg = cv::Mat(480,640,CV_8UC3,cv::Scalar(0, 0, 0));//bufHight,bufWidth
                        int size = cvoutImg.cols * cvoutImg.rows * cvoutImg.channels();
                        
                        memcpy((char*)cvoutImg.data, pBox->ch,size);
                        cv::imshow("read...",cvoutImg);

                        // std::cerr << "cvoutImg::" <<  (cvoutImg) << std::endl;


                        int key = cv::waitKey(30);

                        if (key == 'q') {
                            break;
                        }
		// 	pBox->flag = 0;
		// }       
	}
	
	shmdt(shm);
	shmctl(shmid, IPC_RMID, 0);
	return 0;
} 

```
