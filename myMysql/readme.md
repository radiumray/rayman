
```bash
# 创建镜像
docker build . -t docker-mysql

# 启动容器
docker run -d -p 3366:3306 docker-mysql

# 进入容器
docker exec -it 你获取的容器id /bin/bash


# 使用docker用户登录数据库：
mysql -u docker -p
123456

# 切换至docker_mysql数据库：
use docker_mysql;

# 查看数据库中的表：
show tables;

# 查看表中的数据：
select * from user;


```



# windows 的 Mysql dockerfile制作

## 1、编写Dockerfile

```bash
FROM mysql:5.7.24
# 维护者信息
MAINTAINER liu
 
# 设置root初始化密码
ENV MYSQL_ROOT_PASSWORD=123456
# 设置mysql字符集
ADD mysql.cnf /etc/mysql/mysql.conf.d/my.cnf
 
EXPOSE 3306


```

## 2、编写mysql.cnf文件
lower_case_table_names=1 设置全部小写

```bash

[client]
default-character-set=utf8
 
[mysql]
default-character-set=utf8
 
[mysqld]
init_connect='SET collation_connection = utf8_unicode_ci'
init_connect='SET NAMES utf8'
character-set-server=utf8
collation-server=utf8_unicode_ci
skip-character-set-client-handshake
lower_case_table_names=1 
 
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION

```


## 3、编写快速构建脚本  buildDocker.bat

```bash

::打包镜像
docker build -t com/liu/mysql .
	
::推镜像
::docker push  com/liu/mysql
	
::展示镜像
docker images
	
pause
```

## 4、启动

```bash
#冒号前面3306是主机端口，冒号后面的3306是容器内部端口
docker run -p 3306:3306 -d com/liu/mysql 
```