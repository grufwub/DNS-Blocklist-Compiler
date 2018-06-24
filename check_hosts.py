# TODO: optimize this so much more... Using compile.process_hosts() isn't the most efficient way. And other parts too!

import os, compile
from urllib.request import urlopen, URLError, HTTPError

__HOSTS_FILE = 'hosts'
__CHECKED_HOSTS_FILE = 'checked_hosts'
__NO_PING_CHECKS = 3

def extract_hosts_from_file(filename):
    hosts = dict()
    raw = str()

    f = open(filename, 'r', encoding='utf-8')
    for line in f.readlines():
        raw += line + '\n'
    f.close()

    hosts = compile.process_hosts(raw)
    
    return hosts

def ping_host(host):
    try:
        url = 'http://' + host
        response = urlopen(url)
    except HTTPError:
        return False
    except URLError:
        return False
    except Exception as e:
        print('Exception with host %s' % host)
        print(e)
    
    return True

def run():
    print('\n---------- Hosts Checker ---------')
    print('[pings all the hosts in a file to see which domains are alive]')
    if not os.path.exists(__HOSTS_FILE):
        print('Hosts file does not exist!\nExiting...')
        return

    print('Extracting hosts from file...')
    hosts = extract_hosts_from_file(__HOSTS_FILE)

    before_count = len(hosts)
    print('Pinging hosts... [please wait this may take a while!]')

    for i in range(__NO_PING_CHECKS):
        for host in hosts.keys():
            host_dict = hosts[host]
            for individual_host in host_dict:
                result = ping_host(host)
                if result == False:
                    hosts[host][individual_host] += 1
    
    print('Writing checked hosts to new file %s' % __CHECKED_HOSTS_FILE)
    after_count = 0
    f = open(__CHECKED_HOSTS_FILE, 'w', encoding='utf-8')
    for host in hosts.keys():
        host_dict = hosts[host]
        for individual_host in host_dict:
            if host_dict[individual_host] == __NO_PING_CHECKS - 1:
                continue
            f.write('127.0.0.1 ' + individual_host + '\n')
            after_count += 1
    f.close()

    print('Finished counting %d entries and discarding %d' % (after_count, before_count - after_count))

if __name__ == '__main__':
    run()