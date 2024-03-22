
## muskingum

```python

import numpy as np
import matplotlib.pyplot as plt

# 定义Muskingum算法函数
def muskingum_simulation(input_flow, k, x):
    """
    input_flow: 输入的流量时间序列
    k: Muskingum参数，描述河段之间的水流传输速率
    x: Muskingum参数，描述水流的传播时间延迟
    """
    n = len(input_flow)
    output_flow = np.zeros(n)  # 初始化输出流量时间序列
    
    for i in range(1, n):
        # 计算当前时刻的输出流量
        output_flow[i] = input_flow[i] + (k * (1 - x) * (input_flow[i] - input_flow[i-1]) 
                                           + k * x * (input_flow[i-1] - input_flow[i-2]) 
                                           + (1 - k) * output_flow[i-1])
    
    return output_flow

# 定义输入流量时间序列
input_flow = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])

# 定义Muskingum参数
k = 0.5  # 水流传输速率参数
x = 0.5  # 传播时间延迟参数

# 使用Muskingum算法进行模拟
output_flow = muskingum_simulation(input_flow, k, x)

# 绘制输入和输出流量时间序列
plt.plot(input_flow, label='Input Flow')
plt.plot(output_flow, label='Output Flow')
plt.xlabel('Time')
plt.ylabel('Flow')
plt.title('Muskingum Simulation')
plt.legend()
plt.show()

```


```
