# coding=utf-8
# author: zhangyiling
# 获取系统信息


import requests
import psutil
import subprocess
import socket
import json
import time
import re
import platform

device_white = ['eth0', 'eth1', 'eth2', ]


def get_hostname():
    # 获取主机名
    return socket.gethostname()


def get_innerIp(ipinfo):
    # 获取ip地址
    inner_device = ['eth0', ]
    ret = {}
    for info in ipinfo:
        if info.get('ip', None) and info.get('device', None) in inner_device:
            ret['inner_ip'] = info['ip']
            ret['mac_address'] = info['mac']
            return ret
    return {}


def get_device_info():
    # 获取网卡设备名
    # [{'device': 'eth0', 'ip': '172.16.18.88', 'mac': '00:0c:29:08:79:0c'}]
    ret = []
    for device, info in psutil.net_if_addrs().items():
        if device in device_white:
            device_info = {'device': device}
            for snic in info:
                if snic.family == 2:
                    device_info['ip'] = snic.address
                elif snic.family == 17:
                    device_info['mac'] = snic.address
            ret.append(device_info)
    return ret


def get_cpuinfo():
    # 获取cpu信息
    ret = {'cpu': '', 'num': 0}
    with open('/proc/cpuinfo') as f:
        for line in f:
            line_list = line.strip().split(':')
            key = line_list[0].strip()
            if key == 'model name':
                ret['cpu'] = line_list[1].lstrip()
            if key == 'processor':
                ret['num'] += 1
        return ret


def get_disk():
    # 获取总磁盘空间
    cmd = "/sbin/fdisk -l | egrep 'Disk|Platte'|egrep -v 'identifier|mapper|Disk label'"
    '''
    Disk /dev/sda: 12.9 GB, 12884901888 bytes
    Disk /dev/sdb: 10.7 GB, 10737418240 bytes
    '''
    disk_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    partition_size = []
    for dev in disk_data.stdout.readlines():
        size = int(dev.strip().decode().split(', ')[1].split()[0]) / 1024 / 1024 / 1024
        partition_size.append(str(size))
    return " + ".join(partition_size)


def get_mem():
    # 获取内存总容量
    pc_mem = psutil.virtual_memory()
    div_gb_factor = (1024 ** 3)
    return float('%.2f' % (pc_mem.total / div_gb_factor))


# 获取linux系统信息函数-开始-1
def getDmi():
    p = subprocess.Popen(['dmidecode'], stdout=subprocess.PIPE)
    data = p.stdout.read().decode()
    return data


def parseDmi(data):
    lines = []
    line_in = False
    dmi_list = [i for i in data.split('\n') if i]
    for line in dmi_list:
        if line.startswith('System Information'):
            line_in = True
            continue
        if line_in:
            if not line[0].strip():
                lines.append(line)
            else:
                break
    return lines


def get_Manufacturer():
    # linux系统信息
    dmi_dic = {}
    data = getDmi()
    lines = parseDmi(data)
    dic = dict([i.strip().split(': ') for i in lines])
    dmi_dic['manufacturers'] = dic['Manufacturer']
    dmi_dic['server_type'] = dic['Wake-up Type']
    dmi_dic['sn'] = dic['Serial Number']
    dmi_dic['uuid'] = dic['UUID']
    return dmi_dic


# 获取linux系统信息函数-结束-1

def get_rel_date():
    # 获取出厂日期
    cmd = "/usr/sbin/dmidecode | grep  'Release'"
    data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date = data.stdout.readline().decode().split(': ')[1].strip()
    return re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', date)


def get_os_version():
    # 获取系统版本
    return ' '.join(platform.linux_distribution())


def run():
    # 运行函数
    data = {}
    data['hostname'] = get_hostname()
    data.update(get_innerIp(get_device_info()))
    cpuinfo = get_cpuinfo()
    data['server_cpu'] = '{cpu} {num}'.format(**cpuinfo)
    data['server_disk'] = get_disk()
    data['server_mem'] = get_mem()
    data.update(get_Manufacturer())
    data['manufacture_date'] = get_rel_date()
    data['os'] = get_os_version()
    try:
        if 'VMware' in data['manufacturers']:
            data['vm_status'] = 0
        else:
            data['vm_status'] = 1
    except KeyError:
        raise Exception('run is root')
    print(data)
    send(data)


def send(data):
    # 提交采集信息
    url = 'http://172.16.18.88/resources/server/report/'
    r = requests.post(url, data=data)
    print(r.status_code)
    print(r.content)


if __name__ == '__main__':
    run()
