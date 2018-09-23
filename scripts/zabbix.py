# coding=utf-8
# auth: zhangyiling
# time: 2018/9/8 上午1:50
# description: zabbix_api


import json
import requests

url = 'http://172.16.18.88:99/zabbix/api_jsonrpc.php'
headers = {'Content-Type': 'application/json-rpc'}


def apiinfo():
    """获取zabix版本"""
    data = {
        "jsonrpc": "2.0",
        "method": "apiinfo.version",
        "id": 1,
        "auth": None,
        "params": {},
    }

    r = requests.get(url, headers=headers, data=json.dumps(data))
    print(r.status_code)
    print(r.content)
    print(r.json())


def userlogin():
    """获取登陆token"""
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",
            "password": "888888"
        },
        "id": 1,
        "auth": None
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.status_code)
    print(r.content)
    print(r.json())  # {'jsonrpc': '2.0', 'result': '72b7ced8bc8ad8591f49ee71b050452a', 'id': 1}


def action():
    """获取主机信息"""
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "host", ],
            "selectInterfaces": ["ip", ],
        },
        "auth": "72b7ced8bc8ad8591f49ee71b050452a",
        "id": 1
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.status_code)
    # print(r.content)
    print(json.dumps(r.json()))



if __name__ == '__main__':
    # apiinfo()
    # userlogin()
    action()