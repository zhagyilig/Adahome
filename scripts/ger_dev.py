import psutil


device_white = ['eth0', 'eth1', 'eth2', ]


def get_device_info():
    # 获取网卡设备名
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
    print(ret)
    return ret


get_device_info()
