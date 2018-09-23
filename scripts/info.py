

import subprocess

def get_Manufacturer():
    cmd = '/usr/sbin/dmidecode'
    man_data = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ret = []
    
    for str_line in man_data.stdout.readlines():
        print(str_line)
'''
        for line in str_line.strip().decode():
            print(line)
            if 'UUID' in line:
                print(line)
                ret['uuid'] = line.split(': ')[1].strip()
    print(ret)
    #return ret
'''
get_Manufacturer()


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
