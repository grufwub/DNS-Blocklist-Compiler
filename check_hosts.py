# TODO: optimize this so much more... Using compile.process_hosts() isn't the most efficient way. And other parts too!

import os, compile
from threading import Thread
from queue import Queue
from platform import system as system_name
from subprocess import call as system_call

__HOSTS_FILE = 'hosts'
__CHECKED_HOSTS_FILE = 'checked_hosts'
__NO_PING_CHECKS = 3
__NO_THREADS = 8

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
    param = '-n' if system_name().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return system_call(command) == 0

class PingWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.QUEUE = queue
        self.RESULTS = dict()

    def run(self):
        while True:
            host = self.QUEUE.get()
            if not host: break
            is_live = ping_host(host)
            append_result = 1 if is_live else 0
            self.RESULTS[host] = self.RESULTS.get(host, 0) + append_result
            self.QUEUE.task_done()

    def get(self):
        return self.RESULTS

def run():
    print('\n---------- Hosts Checker ---------')
    print('[pings all the hosts in a file to see which domains are alive]')
    if not os.path.exists(__HOSTS_FILE):
        print('Hosts file does not exist!\nExiting...')
        return

    print('Extracting hosts from file...')
    hosts = extract_hosts_from_file(__HOSTS_FILE)

    before_count = 0
    print('Pinging hosts... [please wait this may take a while!]')
    queue = Queue()
    threads = list()
    for i in range(__NO_THREADS):
        t = PingWorker(queue)
        t.start()
        threads.append(t)

    for host in hosts.keys():
        host_dict = hosts[host]
        for individual_host in host_dict:
            queue.put(individual_host)
            before_count += 1

    queue.join() # Block until all tasks are done

    results = dict()
    for t in threads:
        ret = t.get()
        results.update(ret)
    
    print('Writing checked hosts to new file %s' % __CHECKED_HOSTS_FILE)
    after_count = 0
    f = open(__CHECKED_HOSTS_FILE, 'w', encoding='utf-8')
    for host in results.keys():
        if results[host] != 0:
            f.write('127.0.0.1 ' + individual_host + '\n')
            after_count += 1
    f.close()

    print('Finished counting %d entries and discarding %d' % (after_count, before_count - after_count))

if __name__ == '__main__':
    run()