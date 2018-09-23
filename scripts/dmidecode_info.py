from subprocess import Popen, PIPE

def getDmi():
    p = Popen(['dmidecode'], stdout=PIPE)
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

def dmiDic():
    dmi_dic = {}
    data = getDmi()
    lines = parseDmi(data)
    dic = dict([i.strip().split(': ') for i in lines])
    dmi_dic['vendor'] = dic['Manufacturer']
    dmi_dic['product'] = dic['Product Name']
    dmi_dic['sn'] = dic['Serial Number']
    return dmi_dic

if __name__ == '__main__':
    print(dmiDic())
