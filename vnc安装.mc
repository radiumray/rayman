

cmds.txt
```bash
sudo apt-get install x11vnc
sudo apt install net-tools
x11vnc -storepasswd

sudo cp vnc_server.conf /etc/supervisor/conf.d

sudo supervisorctl reload

```



vnc_server.conf
```bash

# 编辑脚本内容
; 设置进程的名称，使用 supervisorctl 来管理进程时需要使用该进程名
[program:vnc_server]

directory=/home/lamb/.vnc

command=x11vnc -auth guess -forever -loop -noxdamage -repeat -rfbauth /home/lamb/.vnc/passwd -rfbport 5900 -shared

user=mo
numprocs=1
autostart=true
autorestart=true
stdout_logfile=/home/lamb/.vnc/supervisor-out.log
stderr_logfile=/home/lamb/.vnc/supervisor-error.log
stdout_logfile_backups=10

redirct_stderr=true
startsecs=5
stopasgroup=true



```


客户端安装：
RemoteRipple-1.0.4-setup.exe


