#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import Environment
from jinja2 import FileSystemLoader
from boto.ses.connection import SESConnection
from setting import AWSID
from setting import AWSKEY
from setting import LEADER_MAIL
import sys
import csv

ses = SESConnection(AWSID, AWSKEY)
env = Environment(loader=FileSystemLoader('./templates/'))


def gettestinfo():
    ''' 取得測試用資料 '''
    u = {
        'nickname': u'Toomore Chiang',
        'mail': u'toomore0929@gmail.com',
        'leaderno': '8',
    }
    return u


def send_welcome(info):
    ''' 發送歡迎信
        :info: dict 包含 [mail, nickname, leaderno]
    '''
    ses.send_email(
        source='Toomore Chiang <toomore0929@gmail.com>',
        subject=u'COSCUP2013 歡迎你 - {nickname}'.format(**info),
        to_addresses='{mail}'.format(**info),
        cc_addresses='{0}'.format(LEADER_MAIL[info.get('leaderno')]),
        format='html',
        return_path='toomore0929@gmail.com',
        reply_addresses=[
            'toomore0929@gmail.com',
            LEADER_MAIL[info.get('leaderno')]],
        body=template.render(**info),
    )


def send_first(info):
    ''' 發送登錄信
        :info: dict 包含 [mail, nickname]
    '''
    ses.send_email(
        source='Toomore Chiang <toomore0929@gmail.com>',
        subject=u'COSCUP2013 請先完成資料登錄 - {nickname}'.format(**info),
        to_addresses='{mail}'.format(**info),
        format='html',
        return_path='toomore0929@gmail.com',
        reply_addresses='toomore0929@gmail.com',
        body=template.render(**info),
    )


def send_weekly(no, html, mail='toomorebeta@googlegroups.com'):
    ''' 發送週報
    '''
    ses.send_email(
        source='Toomore Chiang <toomore0929@gmail.com>',
        subject=u'COSCUP2013 Weekly #{0:02}'.format(no),
        to_addresses='{0}'.format(mail),
        format='html',
        body=html,
    )

def read_csv(f):
    c = csv.DictReader(f.readlines())
    for i in c:
        for v in i:
            i[v] = unicode(i[v], 'utf-8')
        yield i

def output(u):
    ''' 匯出電子報檔案 htm '''
    with open('/run/shm/ppaper.htm', 'w') as f:
        f.write(template.render(u).encode('utf-8'))


def sendall(sendlist, send):
    ''' 大量傳送 '''
    for i in sendlist:
        try:
            send(i)
            print u'SEND: {}'.format(i)
        except Exception as e:
            print u'ERROR: {}, {}'.format(i, e)


if __name__ == '__main__':
    '''
    python ./t.py output|send|sendall template_files
    '''
    if sys.argv[1] == 'output':
        print u'{0:-^30}'.format(u'匯出電子報')
        template = env.get_template(sys.argv[2])
        output(gettestinfo())
    elif sys.argv[1] == 'send_welcome':
        print u'{0:-^30}'.format(u'寄送歡迎信')
        template = env.get_template('./coscup_sendwelcome.htm')
        send_welcome(gettestinfo())
    elif sys.argv[1] == 'send_first':
        print u'{0:-^30}'.format(u'寄送登錄信')
        template = env.get_template('./coscup_first.htm')
        send_first(gettestinfo())
    elif sys.argv[1] == 'sendall':
        print u'{0:-^30}'.format(u'大量傳送電子報')
        template = env.get_template(sys.argv[2])
        sendall([gettestinfo(), ])
    else:
        print 'output, send, sendall'
    print sys.argv
