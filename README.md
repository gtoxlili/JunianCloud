# JunianCloud

一个轻量、便捷的个人网盘。
A lightweight, convenient personal network disk.

---
## Demo：

[橘年图床](https://api.juniancc.top/uploads#/)

## 项目介绍：

一个基于 vue (前端) 、flask (后端) 的一键式部署网盘。

## 项目实现：

- [x] 基本上传下载功能实现
- [x] 流式下载文件
- [X] 移动端布局适配
- [x] 好看的页面和交互效果(大雾
- [x] 提供了 mysql 和 纯 json 两种形式的存储方式供用户选择
- [ ] 针对媒体,文本文件的弹窗显示

## 如何部署：

#### 安装Docker-CE
```bash
curl -fsSL get.docker.com | bash
```
#### 运行
``` bash
# 如果不想占用宿主的80端口,使用`-p 你想要的端口:80`替换
docker run -d --name=juniancloud \
              -p 80:80 \
	      -v 你需要保存内容的目录的绝对路径:/app/uploads \
	      --restart=always \
	      glovecc/juniancloud
```

## 环境变量:

| 变量名称     | 默认值   | 备注                           |
| ------------ | -------- | ------------------------------ |
| NAME         | 橘年图床 | 设定图床的名称                 |
| DRIVER       | json     | 选择存储的驱动(可选json/mysql) |
| MYSQL_HOST   |          | MYSQL服务器地址                |
| MYSQL_USER   |          | MYSQL用户名                    |
| MYSQL_PASSWD |          | MYSQL密码                      |
| MYSQL_PORT   |          | MYSQL端口                      |
| MAXSIZE      | 100      | 单位MB.默认最大上传100MB.      |

* 环境变量的使用办法:添加如 `-e DRIVER=mysql` `-e MYSQL_HOST`等等参数到部署命令行里面`glovecc/juniancloud` 的前面一起运行即可.
* 如果不需要改变的话不需要添加环境变量保持默认值即可.
* 如果需要使用`mysql`作为存储驱动的话.需要同时设置`DRIVER`以及所有`MYSQL`开头的变量

### 通过 Nginx来反向代理网站(附加):

如果有域名的话还可以试试接下来这步,

``` bash
cd /etc/nginx/conf.d
vim jncloud.conf
```
将以下内容添加到 conf 中：

- http：
如果希望部署到http
``` conf
server {
    listen 80;
    server_name api.juniancc.top; # 域名

    location / {
        proxy_pass http://127.0.0.1: 端口; # 这里是指向 docker 后端的服务地址
        proxy_set_header Host $http_host;
	    proxy_set_header X-Forward-For $remote_addr;
	    client_max_body_size   100m; # 允许的最大上传大小
    }
}
```

- https：
如果希望部署到https
``` conf

server {
    listen 80 default;
    server_name _;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl http2;
    server_name api.juniancc.top; # 域名
    ssl_certificate cert/api.pem; # 域名商那颁发的 https证书
    ssl_certificate_key  cert/api.key; # 同上
    ssl_session_timeout 5m;
    ssl_ciphers EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1: 端口; # 这里是指向 dock 的服务地址
        proxy_set_header Host $http_host;
	    proxy_set_header X-Forward-For $remote_addr;
	    client_max_body_size   100m; # 允许的最大上传大小
    }
}
```
最后，

``` bash
service nginx restart
```

## 最后的最后：

^_^  感谢 [FAN VINGA](https://github.com/fanvinga) 的帮助

Docker 相关推荐阅读：[Docker —— 从入门到实践](https://yeasy.gitbooks.io/docker_practice/container/)

