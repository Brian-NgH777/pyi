import os
import socket    
import multiprocessing
import subprocess
import os
import time
from datetime import date

def ipScan():
    hostname=socket.gethostname()   
    ip=socket.gethostbyname(hostname)
    return ip

def portScan(t_IP):
    port_list = list()
    for i in range(0, 65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
        conn = s.connect_ex((t_IP, i))
        if(conn == 0) :
            port_list.append(i)
            print ('Port %d: OPEN' % (i,))
        s.close()
       
    return port_list


def pinger(job_q, results_q):
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            portList = portScan(ip)
            results_q.put((ip, portList))
        except:
            pass

def map_network(pool_size=255):
    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = ipScan().split('.')
    print ('IP %s' % (ip_parts))
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    # cue hte ping processes
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    # collect he results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list


if __name__ == '__main__':
    multiprocessing.freeze_support()
    print('Mapping...')
    startTime = time.time()
    lst = map_network()
    endTime = time.time()
    totalTime = endTime - startTime
    print(totalTime, lst)

    data= "'%s':%s" %(date.today(), "{'%s':%s, '%s':%s}" %('time', totalTime, 'data', lst))
    log_text = '{}\n'.format(data)

    out_file = open("{}.log".format('data-storage'), "a") 
    out_file.write(log_text)
    out_file.close() 