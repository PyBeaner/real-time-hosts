# encoding=utf-8
import os, sys

def ping(host):
    print('pinging host:{host}'.format(host=host))
    try:
        os.system('ping {host} > ping.tmp'.format(host=host))
        with open('ping.tmp', 'r') as tmp:
            if tmp.read().find('Request timed out') == -1:
                return True
    except:
        print(sys.exc_info())

def get_hosts_path():
    if sys.platform.startswith('win'):
        return r'C:\Windows\System32\Drivers\etc\hosts'
    if sys.platform.startswith('linux'):
        return '/etc/hosts'
    else:
        raise NotImplementedError

def backup_hosts():
    import shutil
    shutil.copyfile(get_hosts_path(), 'hosts.bak')
