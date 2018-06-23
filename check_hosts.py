import os, compile
from urllib.request import urlopen, URLError, HTTPError

__HOSTS_FILE = 'hosts'
__CHECKED_HOSTS_FILE = 'checked_hosts'
__NO_PING_CHECKS = 3

def extract_hosts_from_file(filename):
    hosts = dict()
    raw = str()

    f = open(filename, 'r', encoding='utf-8')
    looping = True
    while (looping):
        # Hacky workaround since it only seemed to be reading one char at a time?
        for content in f.read():
            if content == None:
                looping = False
                break
            if content == '\n':
                break
            raw += content
        raw += '\n'

    f.close()

    hosts = compile.process_hosts(raw)
    
    return hosts

def ping_host(host):
    try:
        response = urlopen(host)
    except HTTPError or URLError:
        return False
    
    return True

def run():
    print('\n---------- Hosts Checker ---------')
    print('[pings all the hosts in a file to see which domains are alive]')
    if not os.path.exists(__HOSTS_FILE):
        print('Hosts file does not exist!\nExiting...')
        return

    print('Extracting hosts from file...')
    hosts = extract_hosts_from_file(__HOSTS_FILE)
    print(hosts)
    before_count = len(hosts)
    print('Pinging hosts...')
    for host in hosts.keys():
        print(host)
        result = ping_host(host)
        print('ping %s result = %d' % host, result)
        if result == True:
            hosts[host] += 1
    
    # print('Writing checked hosts to new file %s' % __CHECKED_HOSTS_FILE)
    # after_count = 0
    # f = open(__CHECKED_HOSTS_FILE, 'w', encoding='utf-8')
    # for host in hosts.keys():
    #     if hosts[host] > 0:
    #         continue
    #     f.write(host + '\n')
    #     after_count += 1
    # f.close()

    # diff = before_count - after_count
    # print('Finished counting %d entries and discarding %d' % after_count, diff)