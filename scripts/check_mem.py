# coding=utf-8
# auth: zhangyiling

"""
import commands
import requests
import json
import xmlrpclib
import socket
import time


def getNowTime():
    return time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))


def dingding(message, phone=[]):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=f0399832b73a0e2fb9503bc2725de96462cc8e04cb47eeb79605e76a6214a894'
    wechat_url = 'http://wechat.65dg.me/robot/send?access_token=db08e4311793c7918a139abf7ac891bf'
    at_mobiles = ['13632623659', '13156519647']
    if phone:
        for p in phone:
            at_mobiles.append(p)
    headers = {'Content-Type': 'application/json'}
    hostname = socket.gethostname()
    info = "hostname:%s\n%s" % (hostname, message)
    data = {
        "msgtype": "text",
        "text": {
            "content": info,
        },
        "at": {
            "atMobiles": at_mobiles,
        }
    }
    # requests.post(url,headers=headers,data=json.dumps(data),timeout=3)
    requests.post(wechat_url, headers=headers, data=json.dumps(data), timeout=3)


def goservice_info(service_name):
    cmdb_url = 'http://192.168.10.161:5001/api/goserviceInfo'
    cmdb_headers = {'Content-Type': 'application/json'}
    cmdb_data = {
        "username": "jenkins",
        "password": "e8cbb7a86ec15012eda2f009ebb50c29",
        "service_name": service_name
    }
    response = requests.post(cmdb_url, headers=cmdb_headers, data=json.dumps(cmdb_data)).text
    result = json.loads(response)['result']
    print
    'phone number: ', result
    return result if result else None


# limit 3G 3145728
def get_process():
    run_cmd = '''ps aux | awk '{if($6>3145728){print $6,$2,$1}}' | sort -n -k 1 -r | egrep -v USER'''  # mem pid user
    msg = commands.getoutput(run_cmd).split('\n')
    return msg if msg[0] else None

    # return msg


def get_supervisor():
    getNowTime()
    server = xmlrpclib.Server('http://admin:ezbuyisthebest@127.0.0.1:29001/RPC2')
    proc = get_process()
    if proc:
        for p in proc:
            info = server.supervisor.getAllProcessInfo()
            mem, pid, user = p.split(' ')
            print
            '-----------', mem, pid, user
            tag = 0
            for i in info:
                if i['pid'] == int(pid):
                    # print i
                    tag = 1
                    phone = goservice_info(i['name'])
                    if i['name'] == 'spk_service_item_cn' and int(mem) > 20971520:
                        info = "memory limit increase: 20G\nuse memory:%sK\nsupervisor_name:%s\naction: warnning" % (
                        mem, i['name'])

                    elif i['name'] == 'spk_service_item_cn':
                        tag = 2
                    else:
                        server.supervisor.stopProcess(i['name'])
                        server.supervisor.startProcess(i['name'])
                        info = "memory limit increase: 3G\nuse memory:%sK\nsupervisor_name:%s\naction: restart %s" % (
                        mem, i['name'], i['name'])
                    if tag == 1:
                        print
                        phone, info
                        dingding(info, phone)
                    break
            if tag == 0:
                print
                'not exists..'
                pid_info = str(commands.getoutput("cat /proc/{}/cmdline".format(pid)).replace("\x00", " "))
                info = "memory limit increase: 3G\nuse memory:%sK\ncmd_line:%s" % (mem, pid_info)
                print
                info
                dingding(info)


get_supervisor()

"""