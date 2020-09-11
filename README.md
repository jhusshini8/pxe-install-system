
#database table coding
alter table InstallRecord convert to character set utf8mb4 collate utf8mb4_bin;

cobbler pxe ubuntu 网卡启动项
cobbler profile edit --name ubuntu-18.04-x86_64 --kopts='interface=auto'

cobbler pxe centos 设置网卡名称
cobbler profile edit --name centos-6.4-x86_64 --kopts='net.ifnames=0 biosdevname=0' 

ubuntu16 启动项
cobbler profile edit --name ubuntu-16.04-x86_64 --kopts='interface=auto  GRUB_CMDLINE_LINUX_DEFAULT="quiet splash text"'

#debian启动内核更换
wget http://ftp.es.debian.org/debian/dists/jessie/main/installer-amd64/current/images/netboot/netboot.tar.gz
mkdir -p /data/images/debian8-amd64
tar zxvf netboot.tar.gz -C /data/images/debian8-amd64
cobbler distro edit --name=debian8.3-x86_64 --kernel=/data/images/debian8-amd64/debian-installer/amd64/linux --initrd=/data/images/debian8-amd64/debian-installer/amd64/initrd.gz



# vue打包正式环境
npm run build:prod