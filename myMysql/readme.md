
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

