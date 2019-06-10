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
how to deploy?
1. 将代码下载到本地或服务器端

``` bash
# download the code to a local or server
git clone https://github.com/Glovecc/JunianCloud

```
2. 根据喜好修改[配置文件](configuration.yaml)

如果刚没放上服务器的现在可以放上去了

3. 运行[一键部署脚本](start.sh)

``` bash

sudo chmod +x start.sh

sh start.sh
```
如果无报错走完了第三步，试试访问 ` 服务器IP : 8080 `

4. 通过 Nginx来反向代理网站(附加)

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
        proxy_pass http://127.0.0.1:8080; # 这里是指向 gunicorn host 的服务地址
        proxy_set_header Host $http_host;
	    proxy_set_header X-Forward-For $remote_addr;
	    client_max_body_size   100m; 
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
        proxy_pass http://127.0.0.1:8080; # 这里是指向 gunicorn host 的服务地址
        proxy_set_header Host $http_host;
	    proxy_set_header X-Forward-For $remote_addr;
	    client_max_body_size   100m; 
    }
}
```
最后，

``` bash
service nginx restart
```

## 最后的最后：

^_^

