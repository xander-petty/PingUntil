"""
The purpose of this tool is intended to open continuous ping until it fails 
a certain number of times consecutively. 
"""
__author__ = 'Xander Petty'
__contact__ = 'Alexander.Petty@williams.com'
__version__ = '1.0'

from scapy.all import IP, ICMP, sr1 
from socket import gethostbyname as nslookup
from socket import gethostbyaddr as reverse_lookup
from time import sleep

# BUILD NOTE - Constructing the backend as a class with functions first
class PingUntil():
    def __init__(self, ip, trigger):
        self.ip = ip 
        self.trigger = trigger
    def _craft_packet(self, ip, ttl):
        packet = IP(dst=ip, ttl=ttl)/ICMP()
        return packet 
    def run(self):
        errors = 0
        success = 0
        while int(errors) != int(self.trigger):
            # Rate limiting the amount of ICMPs to be sent.
            sleep(1)
            packet = self._craft_packet(self.ip, ttl=32)
            reply = sr1(packet, timeout=10, verbose=False)
            if reply == None:
                errors += 1
            else:
                errors = 0
                success += 1
                print(f'Reply from {reply.src}')
        hops = self.trace()
        last_good_hop = hops[int(len(hops) - 1)]
        return last_good_hop
    def trace(self):
        failed = 0
        ttl = 1
        hops = []
        while failed != 3:
            packet = self._craft_packet(self.ip, ttl=ttl)
            reply = sr1(packet, timeout=2, verbose=False)
            if reply == None:
                failed += 1
            elif reply.src == self.ip:
                break
            else:
                failed = 0
                hops.append(reply.src)
                ttl += 1
        return hops 