#!/bin/sh

pathsdaw=$(dirname $(readlink -f $0))

cd $pathsdaw

pip3 install -r requirements.txt

python3 chushi.py

sed -i "s#thisispath#$pathsdaw#" jncloud.sh

mv jncloud.sh /etc/rc.d/init.d/jncloud.sh

cd /etc/rc.d/init.d/

sudo chmod +x jncloud.sh

chkconfig --add jncloud.sh

chkconfig jncloud.sh on

/etc/rc.d/init.d/jncloud.sh

echo "Everything is done!"

echo "Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)"



