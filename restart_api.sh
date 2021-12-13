#!/bin/bash

#cstest_ip="118.143.134.91"
#cstest_ip="118.143.141.196"
cstest_ip="118.143.141.199"
api_nginx_port=8050
/sbin/iptables -vnL | grep -q ${cstest_ip}
if [[ `echo $?` != 0 ]]
then
	echo "Adding IPTABLES"
	/sbin/iptables -I INPUT -p tcp --dport ${api_nginx_port} -s ${cstest_ip} -j ACCEPT
fi
echo "Killing manage.py"
kill -9 `ps ax | grep manage.py | grep -Ev grep | awk '{print $1}'`
sleep 3
echo "Runnning manage.py"
/app/myenv/bin/python3 /app/chinadomainchecker/domaindnschecker/manage.py runserver > /app/china_api.log &
echo "China API Restarted"
