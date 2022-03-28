import socket 
from datetime import date
from scapy.all import *

def arp_scan(ip):
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

    ans, unans = srp(request, timeout=2, retry=1)
    result = []
    for sent, received in ans:
        result.append({'IP': received.psrc, 'MAC': received.hwsrc})

    return result

def tcp_scan(ip, ports):
    try:
        syn = IP(dst=ip) / TCP(dport=ports, flags="S")
    except socket.gaierror:
        raise ValueError('Hostname {} could not be resolved.'.format(ip))

    ans, unans = sr(syn, timeout=2, retry=1)
    result = []

    for sent, received in ans:
        if received[TCP].flags == "SA":
            result.append(received[TCP].sport)

    return result

def main():
    cidr= "/24"
    hostname=socket.gethostname()   
    ipAddr=socket.gethostbyname(hostname)
    ip= "%s%s" %(ipAddr, cidr)
    result = arp_scan(ip)

    #  if args.range:
    #         ports = tuple(args.ports)
    #     else:
    #         ports = args.ports
        
    #     try:
    #         result = tcp_scan(args.IP, ports)

    data= "'%s':%s" %(date.today(), result)
    log_text = '{}\n'.format(data)

    out_file = open("{}.log".format('data-storage'), "a") 
    out_file.write(log_text)
    out_file.close() 

if __name__ == '__main__':
    main()