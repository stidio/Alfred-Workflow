# encoding: utf-8

'''
Author:   Nicolas Chow
Contact:  stidio@163.com
Blog:     http://stidio.github.io
Created:  2016-11-21 17:22:51
'''

import sys
from workflow import Workflow, ICON_INFO, ICON_ERROR, web
from commands import getoutput
import socket
from urlparse import urlparse

def get_location_information(ip):
    '''
    通过IP获取地理位置信息
    '''

    LOCATION_QUERY_URL = 'http://www.ip138.com/ips138.asp'
    FEATURE_BEGIN_STR = '<td align="center"><ul class="ul1"><li>'
    FEATURE_END_STR = '</li></ul></td>'
    FEATURE_SPLIT_STR = '</li><li>'

    try:
        rt = web.get(LOCATION_QUERY_URL, dict(ip=ip, action=2))
        rt.raise_for_status()
        rts = rt.text[
            rt.text.find(FEATURE_BEGIN_STR) + len(FEATURE_BEGIN_STR) : 
            rt.text.find(FEATURE_END_STR)]
        rtlist = rts.split(FEATURE_SPLIT_STR)
        
        # 去掉前缀和多余空格，最长的即是最优解
        result = ''
        for val in rtlist:
            rl = val[val.find(u'：') + 1:].strip().split()
            # 对诸如：北京市北京市 这种字符串修整为：北京市
            for i, k in enumerate(rl):
                size = len(k)
                if size % 2 == 0:
                    size /= 2
                    lhalf = k[:size]
                    rhalf = k[size:]
                    if lhalf == rhalf:
                        rl[i] = lhalf

            temp = ' '.join(rl)
            if len(temp) > len(result):
                result = temp
    except Exception:
        result = None
    
    return result


def get_local_ip():
    '''
    获取本机内网IP
    '''

    return getoutput('ipconfig getifaddr en0')


def get_public_ip():
    PUBLIC_IP_QUERY_URL = 'http://1212.ip138.com/ic.asp'
    try:
        rt = web.get(PUBLIC_IP_QUERY_URL)
        rt.raise_for_status()
        ip = rt.text[rt.text.find('[') + 1 : rt.text.find(']')]
    except Exception:
        ip = None

    return ip


def resolve_ip_from_dns(urlorhost):
    '''
    解析IP地址，可传入IP,HOSTNAME,URL
    '''

    host = urlparse(urlorhost).hostname
    if not host:
        host = urlorhost
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        ip = None

    return host, ip


def main(wf):
    # 去掉参数两边的空格
    param = (wf.args[0] if len(wf.args) else '').strip()
    if param:
        title, ip = resolve_ip_from_dns(param)
    else:
        title = get_local_ip()
        ip = get_public_ip()
    
    if ip:
        location = get_location_information(ip)
        wf.add_item(title=title, 
                    subtitle=ip + ' ' + location if location else '', 
                    arg=ip,
                    valid=True,
                    icon=ICON_INFO)
    else:
        wf.add_item(title=title, subtitle='...', icon=ICON_ERROR)

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))

