#!/bin/bash
##########################set conf############################
#set ulimit
cat >> /etc/security/limits.conf << EOF
 *           soft   nofile       1024000
 *           hard   nofile       1024000
 *           soft   nproc        1024000
 *           hard   nproc        1024000
EOF

#update-grub
apt update -y
apt-get install -y curl

#set ssh
sed -i 's/PermitRootLogin without-password/#PermitRootLogin without-password/' /etc/ssh/sshd_config
sed -i 's/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config
systemctl restart sshd

#set dns
echo "nameserver 10.17.42.200" >> /etc/resolv.conf
echo "nameserver 10.17.42.201" >> /etc/resolv.conf

#set network static
sed -i 's/dhcp/static/g' /etc/network/interfaces
hostip=`ifconfig eth0 | grep "inet addr" | awk '{print $2}' | awk -F':' '{print $2}'`
hostmask=`ifconfig eth0 | grep "inet addr" | awk '{print $4}' | awk -F':' '{print $2}'`
hostgate=`route -n | awk '{print $2}' | awk 'NR==3{print}'`
echo "address $hostip" >> /etc/network/interfaces
echo "netmask $hostmask" >> /etc/network/interfaces
echo "gateway $hostgate" >> /etc/network/interfaces

#Post install system status
host_name=`hostname`
curl -H "Content-Type: application/json" -X POST -d '{"nodename": "'$host_name'", "suctag":2 }' "http://127.0.0.1:8100/api/stagssuc/"

sed -i '/sleep/d' /etc/rc.local
sed -i '/debian8/d' /etc/rc.local
rm -rf /etc/default/debian8.sh
