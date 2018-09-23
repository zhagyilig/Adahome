# coding=utf-8
# auth: zhangyiling
# 模拟生成系统信息,写到cmdb

import random
import struct
import uuid
import requests

"""
{
	'hostname': 'zyl-node1',
	'inner_ip': '172.16.18.88',
	'mac_address': '00:0c:29:08:79:0c',
	'server_cpu': 'Intel(R) Core(TM) i5-5250U CPU @ 1.60GHz 1',
	'server_disk': '12.0 + 10.0',
	'server_mem': 0.96,
	'manufactures': 'VMware, Inc.',
	'product': 'VMware Virtual Platform',
	'sn': 'VMware-56 4d 8b 46 b4 9a 97 ab-3c be 3e a7 00 08 79 0c',
	'uuid': '468B4D56-9AB4-AB97-3CBE-3EA70008790C',
	'manufacture_date': '2015-07-02',
	'os': 'CentOS 6.7 Final',
	'vm_status': 0
}
"""


def get_mac_address():
    mac_bin_list = []
    mac_hex_list = []
    for i in range(1, 7):
        i = random.randint(0x00, 0xff)
        mac_bin_list.append(i)
    Fake_HW = struct.pack('BBBBBB', mac_bin_list[0], mac_bin_list[1],
                          mac_bin_list[2], mac_bin_list[3], mac_bin_list[4], mac_bin_list[5])
    for j in mac_bin_list:
        mac_hex_list.append(hex(j))
    Hardware = ':'.join(mac_hex_list).replace('0x', '')
    return Hardware


def get_uuid():
    return str(uuid.uuid1())


def get_hostname():
    for idc in ['yz', 'jxq', 'ct', 'ct']:
        for bus in ['fang', 'zp', 'sec', 'service', 'pay']:
            for ser in ['web', 'wap', 'app', 'api']:
                for ind in range(1, 10):
                    index = '{:0>2}'.format(ind)
                    hostname = '{}-{}-{}-{}'.format(idc, bus, ser, index)
                    yield hostname


def get_ip_address():
    ip_ = '10.20'
    for ip3 in range(1, 254, 3):
        for ip4 in range(1, 254, 2):
            ip = '{}.{}.{}'.format(ip_, ip3, ip4)
            yield ip


def run():
    hostname = get_hostname()
    ip = get_ip_address()
    data = {}
    data['server_disk'] = '88'
    data['server_type'] = 'VirtualBox'
    data['server_cpu'] = 'Intel(R) Core(TM) i5-5250U CPU @ 1.60GHz 1'
    data['vm_status'] = 1
    data['manufacturers'] = 'VMware, Inc.'
    data['server_mem'] = '699.9 MB'
    data['manufacture_date'] = '2015-07-02'
    data['os'] = 'CentOS 6.7 Final'
    data['sn'] = 'VMware-56 4d 8b 46 b4 9a 97 ab-3c be 3e a7 00 08 79 0c'
    for i in range(1, 800):
        data['uuid'] = get_uuid()
        data['mac_address'] = get_mac_address()
        data['hostname'] = hostname.__next__()
        data['inner_ip'] = ip.__next__()
        send(data)


def send(data):
    """刷新服务器信息"""
    url = 'http://172.16.18.88/resources/server/report/'
    r = requests.post(url, data=data)
    print(r.status_code)
    print(r.content)


if __name__ == '__main__':
    run()
