
import scapy
from scapy.all import *
from scapy.utils import PcapReader
import re
import sys

file = sys.argv[1]

pcap_file = rdpcap(file)
packet_list = []

dictionary = {}

for data in pcap_file:
    # save each packet to a list
    packet_list.append(repr(data))

src_ip = re.compile('src=([0-9]{1,3}\.){3}[0-9]{1,3}')
dst_ip = re.compile('dst=([0-9]{1,3}\.){3}[0-9]{1,3}')

for packet in packet_list:
    src_matches = src_ip.search(packet)
    dst_matches = dst_ip.search(packet)
    if src_matches:
        match1 = src_matches.group()
        # Do split the match string based on '=' as the delimiter
        ip = match1.split('=')[1]
        # If the ip is not in the dictionary then add 1 to it
        if ip not in dictionary:
            dictionary[ip] = 1
        # If the ip is in the dictionary then increment it
        else:
            dictionary[ip] += 1
    if dst_matches:
        match1 = dst_matches.group()
        ip = match1.split('=')[1]
        if ip not in dictionary:
            dictionary[ip] = 1
        else:
            dictionary[ip] += 1
#print(dictionary)
print(packet_list[66])
print(packet_list[67])
print(packet_list[68])
