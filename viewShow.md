
```py

'''
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 360), ylim=(-2, 2))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    x = np.linspace(0, 360, 1000)
    y = np.sin(0.5 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
'''



import numpy as np

import matplotlib

import matplotlib.pyplot as plt

import matplotlib.animation as animation

# # 指定渲染环境

# %matplotlib notebook

# # %matplotlib inline

Id = 0
Iq = 1

theat = np.linspace(0, 360, 1000)

def d2r(degree):
    return degree*np.pi/180

fig = plt.figure(tight_layout=True)
plt.axes(xlim=(0, 360), ylim=(-2, 2))


parkMatric = np.array(
    ([np.cos(d2r(theat)),np.sin(d2r(theat))], 
    [-np.sin(d2r(theat)),np.cos(d2r(theat))]))

dqMatric = np.array(([Id, Iq]))
alpaBetaMatic = np.dot(dqMatric, parkMatric)

alpa = alpaBetaMatic[0]
beta = alpaBetaMatic[1]


clartMatic = np.array(([1, -0.5, -0.5], 
                    [0, np.sqrt(3)/2, -np.sqrt(3)/2]))

abcMatic = np.zeros((3, 1000))

for i in range(1000):
    abcMatic[:, i] = np.dot(alpaBetaMatic[:, i], clartMatic)

print(abcMatic)
# abcMatric = np.dot(alpaBetaMatic, clartMatic)

Ia = abcMatic[0]
Ib = abcMatic[1]
Ic = abcMatic[2]


# plt.plot(theat,alpa)
# plt.plot(theat,beta)


plt.plot(theat,Ia)
plt.plot(theat,Ib)
plt.plot(theat,Ic)

plt.grid(ls="--")

plt.show()

```
