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
apt-get -y install curl net-tools
# set max service processes
cat >> /etc/systemd/system.conf << EOF
DefaultLimitNOFILE=1024000
DefaultLimitNPROC=1024000
EOF

#set ssh
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config
/etc/init.d/ssh restart

#set sysctl
true > /etc/sysctl.conf
cat >> /etc/sysctl.conf << EOF
net.ipv4.ip_forward = 0
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.default.accept_source_route = 0
kernel.sysrq = 0
kernel.core_uses_pid = 1
net.ipv4.tcp_syncookies = 1
fs.file-max = 1024000
fs.nr_open = 1024000
vm.swappiness = 0
vm.max_map_count = 2048000
vm.overcommit_memory = 1
kernel.sem =5010 641280 5010 128
kernel.pid_max = 4194303
kernel.msgmnb = 65536
kernel.msgmax = 65536
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
net.ipv4.tcp_max_tw_buckets = 6000
net.ipv4.tcp_sack = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_mem = 786432 1697152 1945728
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.netdev_max_backlog = 2048000
net.core.somaxconn = 65535
net.ipv4.tcp_max_orphans = 3276800
net.ipv4.tcp_max_syn_backlog = 2048000
net.ipv4.tcp_mem = 94500000 915000000 927000000
net.ipv4.tcp_fin_timeout = 1
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.neigh.default.gc_stale_time=120
net.ipv4.conf.default.rp_filter=0
net.ipv4.conf.all.rp_filter=0
net.ipv4.conf.all.arp_announce=2
net.ipv4.conf.lo.arp_announce=2
EOF
/sbin/sysctl -p
echo "sysctl set OK!!"

#set dns
echo DNS=10.17.42.200 >>/etc/systemd/resolved.conf
echo DNS=10.17.42.201 >>/etc/systemd/resolved.conf
systemctl restart systemd-resolved.service
chmod +x /etc/rc.local

#set network static
sed -i 's/dhcp/static/g' /etc/network/interfaces
hostip=`ifconfig eno1 | grep "inet" | awk '{print $2}' | awk 'NR==1{print}'`
hostmask=`ifconfig eno1 | grep "inet" | awk '{print $4}' | awk 'NR==1{print}'`
hostgate=`route -n | awk '{print $2}' | awk 'NR==3{print}'`
echo "address $hostip" >> /etc/network/interfaces
echo "netmask $hostmask" >> /etc/network/interfaces
echo "gateway $hostgate" >> /etc/network/interfaces

#Post install system status
host_name=`hostname`
curl -H "Content-Type: application/json" -X POST -d '{"nodename": "'$host_name'", "suctag":2 }' "http://127.0.0.1:8100/api/stagssuc/"

sed -i '/sleep/d' /etc/rc.local
sed -i '/debian10/d' /etc/rc.local
rm -rf /etc/default/debian10.sh
