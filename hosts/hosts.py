# encoding=utf-8
import time
import datetime
import os
import requests

from utils import get_hosts_path, backup_hosts


HOST_URL = 'http://tx.txthinking.com/hosts'
SYS_HOSTS_PATH = get_hosts_path()
BLOCK_START = '## updated by Real-Time-Hosts'
BLOCK_END = '## End of Real-Time-Hosts'

def update_hosts(hosts):
    print('updating hosts:{hosts}'.format(hosts=hosts))
    with open(SYS_HOSTS_PATH, 'r') as f:
        sys_hosts = f.read()
    if BLOCK_START not in sys_hosts:
        hosts.insert(0, BLOCK_START)
    if BLOCK_END not in sys_hosts:
        hosts.append(BLOCK_END)
        to_write = sys_hosts + '\n'.join(hosts)
    else:
        import re
        to_write = re.sub(BLOCK_END, '\n'.join(hosts)+'\n'+BLOCK_END, sys_hosts)
    backup_hosts()
    with open(SYS_HOSTS_PATH, 'w') as f:
        f.write(to_write)
    print('update complete')

def retrieve_hosts():
    print('retrieving latest hosts')
    r = requests.get(HOST_URL)
    # hosts = [host.strip() for host in r.text.split('\n')]
    hosts = [host for host in r.text.splitlines() if not host.startswith('#')]
    sys_hosts = open(SYS_HOSTS_PATH).readlines()
    for line in sys_hosts:
        line = line.strip()
        if line in hosts:
            hosts.remove(line)
    return hosts

def monitor():
    while True:
        hosts = retrieve_hosts()
        if hosts:
            update_hosts(hosts)
        else:
            print('hosts is already updated')
        time.sleep(60*30)

if __name__ == '__main__':
    monitor()
