#!/bin/sh
#chkconfig: 2345 20 80
#description:Server reboot.Execute jncloud.sh

cd thisispath

# 启动gunicorn服务

gunicorn  --reload -c gunicorn.conf index:app;
