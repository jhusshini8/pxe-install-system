# -*- coding:utf-8 -*-
from django.http import JsonResponse
from SystemProject import models
import xmlrpc.client
import re
import random
import datetime
import paramiko
import sys, os
import global_settings

def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def isMAC(str):
    if re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", str):
        return True
    else:
        return False

def InstallSystem(request):
    if (request.method == 'POST'):
        postBody = request.body
        ipmistg = 0
        print postBody
        ipadd = eval(postBody).get("nodeip")
        gateadd = eval(postBody).get("nodegate")
        markadd = eval(postBody).get("nodemark")
        if eval(postBody).get("ipmi") == None:
            ipmiadd = "虚拟控制台安装"
            ipmistg = 1
        else:
            ipmiadd = eval(postBody).get("ipmi")
        if eval(postBody).get("ipmipass") == None:
            ipmipas = "虚拟控制台安装"
            ipmistg = 1
        else:
            ipmipas = eval(postBody).get("ipmipass")
        author = eval(postBody).get("author")
        macadd = eval(postBody).get("title")
        macadd = macadd.upper()
        systemtype = eval(postBody).get("type")
        installcontent = eval(postBody).get("remark")
        getip_url = "https://ops.int.jumei.com/api/asset/host/get-by-ipaddr/?ip_addr=%s" % ipadd
        tmpres = os.popen('curl -s %s' % getip_url).readlines()
    try:
        tmpres = tmpres[15].replace(',', '').replace('\n', '').replace('\ ', '')
        tmpres_result = tmpres.split()[1]
    except:
        tmpres_result = 'true'
    if tmpres_result == 'false':
        result = {}
        result["message"] = "IP地址不在OPS资源池中"
        result["status"] = 1
        result["code"] = 20001
        return JsonResponse(result, safe=False)
    else:
        try:
            remote_server = xmlrpc.client.Server(global_settings.server)
            token = remote_server.login(global_settings.user, global_settings.password)
            installip = models.InstallRecord.objects.filter(ipaddr=ipadd)
            installmac = models.InstallRecord.objects.filter(macaddr=macadd)
            for i in installip:
                if int(i.installstatus) == 1:
                    result = {}
                    result["message"] = "IP地址已经在安装中"
                    result["status"] = 1
                    result["code"] = 20001
                    return JsonResponse(result, safe=False)

            for i in installmac:
                if int(i.installstatus) == 1:
                    result = {}
                    result["message"] = "MAC地址已经在安装中"
                    result["status"] = 1
                    result["code"] = 20001
                    return JsonResponse(result, safe=False)

            if remote_server.ping():  # cobbler服务器状态监测
                if eval(postBody).get("nodehostname") in remote_server.find_system():
                    result = {}
                    result["status"] = 1
                    result["code"] = 20001
                    result["message"] = "主机名重复"
                    return JsonResponse(result, safe=False)
                else:
                    #创建
                    random_name = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',8))
                    systype = models.SystemType.objects.get(id=systemtype).record_list
                    system_id = remote_server.new_system(token)
                    remote_server.modify_system(system_id, "name", random_name, token)
                    remote_server.modify_system(system_id, "hostname", random_name, token)
                    remote_server.modify_system(system_id, 'modify_interface', {
                        'macaddress-eth0': macadd.strip(),
                        'ipaddress-eth0': ipadd.strip(),
                        'gateway-eth0': gateadd.strip(),
                        'subnet-eth0': markadd.strip(),
                        'static-eth0': 1,
                    },token)
                    remote_server.modify_system(system_id, "profile", systype, token)
                    remote_server.save_system(system_id, token)
                    # os.system('cobbler system edit --name=%s --gateway=%s' % (random_name, gateadd))
                    remote_server.sync(token)
                    now_time = datetime.datetime.now()
                    # os.system('cobbler system edit --name=%s --gateway=%s' % (random_name,gateadd))
                    # os.system('cobbler sync')
                    if ipmistg == 1:
                        datainsert = models.InstallRecord.objects.create(cobbler_name=random_name, typename=1,
                                                                         ipmiaddr=ipmiadd, ipmipass=ipmipas,
                                                                         version_name_id=systemtype, ipaddr=ipadd,
                                                                         macaddr=macadd, installstatus=1, author=author,
                                                                         installtime=now_time, gateaddr=gateadd,
                                                                         remark_content=installcontent)
                        datainsert.save()
                        result = {}
                        result["status"] = 0
                        result["code"] = 20000
                        return JsonResponse(result, safe=False)
                    else:
                        try:
                            # 创建SSH对象
                            ssh = paramiko.SSHClient()
                            # 允许连接不在know_hosts文件中的主机
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            # 连接服务器
                            ssh.connect(hostname=ipmiadd, port=22, username='root', password=ipmipas)
                            # 执行命令
                            # stdin：标准输入（就是你输入的命令）；stdout：标准输出（就是命令执行结果）；stderr:标准错误（命令执行过程中如果出错了就把错误打到这里），stdout和stderr仅会输出一个
                            stdin, stdout, stderr = ssh.exec_command('racadm config -g cfgServerInfo -o cfgServerBootOnce 1')
                            stdin, stdout, stderr = ssh.exec_command('racadm config -g cfgServerInfo -o cfgServerFirstBootDevice PXE')
                            stdin, stdout, stderr = ssh.exec_command('racadm serveraction powercycle')
                            # stdin, stdout, stderr = ssh.exec_command('racadm serveraction powerstatus')
                            # 获取命令结果
                            result = (stdout.read().decode('utf-8'))  # 这个有问题，如果执行的命令是错误的，会不显示错误，可以修改一下，先判断stdout有没有值，如果输出没有，就显示错误
                            print(result)
                            ssh.close()

                            datainsert = models.InstallRecord.objects.create(cobbler_name=random_name, typename=1, ipmiaddr=ipmiadd, ipmipass=ipmipas,
                                                                             version_name_id=systemtype, ipaddr=ipadd,
                                                                             macaddr=macadd, installstatus=1, author=author,
                                                                             installtime=now_time,gateaddr=gateadd,
                                                                             remark_content=installcontent)
                            datainsert.save()
                        except:
                            remote_server.remove_system(random_name, token)
                            remote_server.sync(token)
                            result = {}
                            result["status"] = 1
                            result["code"] = 20002
                            result["message"] = "IPMI地址不能连接"
                            return JsonResponse(result, safe=False)

                    result = {}
                    result["status"] = 0
                    result["code"] = 20000
                    return JsonResponse(result, safe=False)
            else:
                result = {}
                result["message"] = "安装错误"
                result["status"] = 1
                result["code"] = 20001
                return JsonResponse(result, safe=False)

        except Exception as e:
            print e
            result = {}
            result["message"] = "pxe系统挂球了!!!"
            result["status"] = 1
            result["code"] = 20001
            return JsonResponse(result, safe=False)





    # print(remote_server.get_user_from_token(token))  # 返回cobbler系统登录账号
    # print(remote_server.get_item('distro','Centos6.9-x86_64')) # 获取指定发布版本的信息
    # print('-------------------------')
    # print(remote_server.get_distro('Centos6.9-x86_64'))  #返回distro指定名称的详细信息
    # print('-------------------------')
    # print(remote_server.get_profile('CT6.8_PHY_db_high'))  # 返回profile 指定名称的详细信息
    # print('-------------------------')
    # print(remote_server.get_distros())   # 返回所有distro 的已有内容
    # print('-------------------------')
    # print(remote_server.get_profiles())  # 返回所有profiles的已有内容
    # print('-------------------------')
    # print(remote_server.find_system())  # 以列表返回所有的 system 名称
    # print('-------------------------')
    # print(remote_server.find_distro())  # 以列表返回所有的distro名称
    # print('-------------------------')
    # print(remote_server.find_profile())  # 以列表返回所有profile的名称
    # print('-------------------------')
    # print(remote_server.has_item('distro','Centos6.9-x86_64'))  # 检测指定distro中指定的名称是否存在
    # print('-------------------------')
    # print(remote_server.get_distro_handle('Centos6.9-x86_64',token))  # 没啥用
    # print(remote_server.remove_profile('test111',token))  # 删除指定的profile
    # print('-------------------------')
    # print(remote_server.remove_system('hostname121',token)) # 删除指定的system
    # print('-------------------------')
    # prof_id = remote_server.new_profile(token)  # 创建一个新的profile 并保存
    # print('profile new id:%s' % prof_id)
    # print('-------------------------')
    # remote_server.modify_profile(prof_id,'name','vm_test1',token) # 修改prof_id指定的profile 名称
    # remote_server.modify_profile(prof_id,'distro','centos6.8-x86_64',token)  # 也是修改prof_id的信息
    # remote_server.modify_profile(prof_id,'kickstart','/var/lib/cobbler/kickstarts/txt111',token)
    # remote_server.save_profile(prof_id,token) # 保存
    # remote_server.sync(token) # 同步cobbler修改后的信息，这个做任何操作后，都要必须有
    # print('-------------------------')
    # print(remote_server.get_kickstart_templates())  # 获取所有KS模板文件路径
    # print('-------------------------')
    # print(remote_server.get_snippets())  # 获取所有snippets文件路径
    # print('-------------------------')
    # print(remote_server.is_kickstart_in_use('/var/lib/cobbler/kickstarts/CT6.8_PHY_db_middle.ks')) # 判断ks文件是否在使用
    # print('-------------------------')
    # print(remote_server.generate_kickstart('CT6.8_PHY_web_high')) # 打印profile对应的ks文件内存
    # print('-------------------------')
    # print(remote_server.generate_kickstart('vm_test1','t1'))# 打印profile对应的ks文件内存
    # print('-------------------------')
    # print(remote_server.generate_gpxe('vm_test1')) # 启动方面的，没用
    # print('-------------------------')
    # print(remote_server.generate_bootcfg('vm_test1'))
    # print('-------------------------')
    # print(remote_server.get_blended_data('vm_test1')) # 获取profile 的详细信息
    # print('-------------------------')
    # print(remote_server.get_settings())  # 没啥用
    # print('-------------------------')
    # print(remote_server.get_signatures())  # 不知道输出的是啥
    # print('-------------------------')
    # print(remote_server.get_valid_breeds())  # 获取的是各个操作系统的类型，
    # 输出： ['debian', 'freebsd', 'generic', 'nexenta', 'redhat', 'suse', 'ubuntu', 'unix', 'vmware', 'windows', 'xen']
    # print('-------------------------')
    # print(remote_server.get_valid_os_versions())  # 没啥用
    # print('-------------------------')
    # print(remote_server.get_repo_config_for_profile('vm_test1'))
    # print('-------------------------')
    # print(remote_server.get_repo_config_for_system('t1'))
    # print('-------------------------')
    # print(remote_server.version())  # 返回cobbler版本，没啥用
    # print('-------------------------')
    # print(remote_server.extended_version())  # 返回cobbler详细版本信息，没啥用
    # print('-------------------------')
    # print(remote_server.logout(token))  # 退出当前cobbler连接
    # print('-------------------------')
    # print(remote_server.token_check(token))  # 检测当前token状态，是否失效
    # print('-------------------------')
    # print(remote_server.sync_dhcp(token)  # 同步DHCP
    # print('-------------------------')
    # print(remote_server.sync(token))  # 进行同步更新
    # print('-------------------------')
    # print(remote_server.read_or_write_kickstart_template('cobbler上ks文件路径','false为可写','将要替换ks文件的内容',token))  # 注意 替换KS字符串如果为-1，将删除此Ks文件，条件是此ks文件已不在引用
    # print(remote_server.read_or_write_kickstart_template('/var/lib/cobbler/kickstarts/hostname106.ks',False,-1,token))
    # print('-------------------------')
    # print(remote_server.get_config_data('zhaoyong'))  # 没啥用
    # print('-------------------------')
    # x  = remote_server.test_xmlrpc_ro()
    # print(x.distro)
    # print(remote_server.read_or_write_snippet('/var/lib/cobbler/snippets/test1',False,'zhaoyong_test',token)) # 在snippgets下建立脚本文件
    # distro_obj = cbl_distro.cobbler_distro(remote_server,token)
    # # distro 查询
    # out = distro_obj.find_distro_name()
    # print(out)
    # out = distro_obj.find_distro_info('Centos6.9-x86_64')
    # print(out)
    #
    # profile_obj = cbl_profile.cobbler_profiles(remote_server,token)
    #  profile 查找
    # pro_name_list = profile_obj.find_profile_name()
    # print(out)
    # out = profile_obj.find_profile_info('CT6.8_VM_web_custom')
    # print(out)
    #
    # system_obj = cbl_system.cobbler_system(remote_server,token)
    # # system 查询
    # out_all = system_obj.find_system_name()
    # print(out_all)
    # out = system_obj.system_name_info('tttttt')
    # print(out)
    # del system