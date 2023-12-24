# 这是一个为了学习 Python 的练习项目，没啥实际的用途

## 

sudo docker run -d --restart=always --name quanyy-mysql -v \
/quantyy-mysql-data:/var/lib/mysql \
-p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=Qiqi0202 mysql:8.0.35-bullseye

sudo docker container run -d --restart=always \
  --name nginx \
  --volume "/QuantYY/html":/usr/share/nginx/html \
  --volume "/home/yuanyi/Workspaces/QuantYY/quant_yy_supports/nginx/conf.d":/etc/nginx/conf.d \
  -p 80:80 \
  nginx:latest

sudo docker run -d --restart=always -v /tdengine_prod/data:/var/lib/taos \
  -v /tdengine_prod/logs:/var/log/taos \
  -p 6030:6030 -p 6041:6041 -p 6043-6049:6043-6049 -p 6043-6049:6043-6049/udp \
  --name tdengine_prod tdengine/tdengine:latest



sudo docker run -d --restart=always -v /tdengine_np/data:/var/lib/taos \
  -v /tdengine_np/logs:/var/log/taos \
  -p 16030:6030 -p 16041:6041 -p 16043-16049:6043-6049 -p 16043-16049:6043-6049/udp \
  --name tdengine_np tdengine/tdengine:latest

  ## Database schema

