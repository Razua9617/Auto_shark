import pyshark
from scapy.all import *
import re
import sys

# Read the pcap file, loop over it and save it to a list
def read_sys_argv():
    file = sys.argv[1]
    return file

def read_file():
    file = read_sys_argv()
    pcap_file = rdpcap(file)
    packet_list = []
    for data in pcap_file:
        packet_list.append(repr(data))
    return packet_list

# This function will only return the number of packets
def num_of_packets():
    packets = read_file()
    print(f"Number of Packets: {len(packets)}")

# This function will only get the source IP Addresses
def set_src_ip():
    dictionary = {}
    packet_output = read_file()
    src_ip = re.compile('src=([0-9]{1,3}\.){3}[0-9]{1,3}')
    for packet in packet_output:
        src_matches = src_ip.search(packet)
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
    return dictionary

# get the destination ip addresses only
def set_dst_ip():
    dictionary = {}
    packet_output = read_file()
    dst_ip = re.compile('dst=([0-9]{1,3}\.){3}[0-9]{1,3}')
    for packet in packet_output:
        dst_matches = dst_ip.search(packet)
        if dst_matches:
            match1 = dst_matches.group()
            ip = match1.split('=')[1]
            if ip not in dictionary:
                dictionary[ip] = 1
            else:
                dictionary[ip] += 1
    return dictionary

# This funtion will match the source ip to their mac and their tcp and udp ports
def match_src_ip_mac_TCP_UDP():

    src_ip = re.compile('src=([0-9]{1,3}\.){3}[0-9]{1,3}')
    src_mac = re.compile('src=([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')
    sport = re.compile('sport=([0-9]{1,6}|[a-zA-Z]{1,25})')
    packet_output = read_file()
    ip_mac = {}
    ip = ' '
    for packet in packet_output:
        if "|<IP" in packet:
            ip_matches = src_ip.search(packet)
            mac_matches = src_mac.search(packet)
            if ip_matches and mac_matches:
                match1 = ip_matches.group()
                match2 = mac_matches.group()
                ip = match1.split('=')[1]
                mac = match2.split('=')[1]
                if ip not in ip_mac:
                    ip_mac[ip] = {'MAC':mac,'TCP':[],'UDP':[]}
        if "|<TCP" in packet:
            sport_matches = sport.search(packet)
            if sport_matches:
                match = sport_matches.group()
                port = match.split('=')[1]
                if port not in ip_mac[ip]['TCP']:
                    if port != '':
                        ip_mac[ip]['TCP'].append(port)
        if "|<UDP" in packet:
            sport_matches = sport.search(packet)
            if sport_matches:
                match = sport_matches.group()
                port = match.split('=')[1]
                if port not in ip_mac[ip]['UDP']:
                    if port != '':
                        ip_mac[ip]['UDP'].append(port)
    ip_mac[ip]['TCP'].sort(reverse=True)
    ip_mac[ip]['UDP'].sort(reverse=True)
    return ip_mac

# This function will match the source ip to their mac and their tcp and udp ports
def match_dst_ip_mac_TCP_UDP():

    dst_ip = re.compile('dst=([0-9]{1,3}\.){3}[0-9]{1,3}')
    dst_mac = re.compile('dst=([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')
    dport = re.compile('dport=([0-9]{1,6}|[a-zA-Z]{1,25})')
    packet_output = read_file()
    ip_mac = {}
    for packet in packet_output:
        if "|<IP" in packet:
            ip_matches = dst_ip.search(packet)
            mac_matches = dst_mac.search(packet)
            if ip_matches and mac_matches:
                match1 = ip_matches.group()
                match2 = mac_matches.group()
                ip = match1.split('=')[1]
                mac = match2.split('=')[1]
                if (ip == ' ' and mac == ' ') or (ip == ' ' or mac == ' '):
                    ip = 'IP NOT FOUND'
                    ip_mac[ip] = {'MAC':mac,'TCP':[],'UDP':[]}
                elif ip not in ip_mac:
                    ip_mac[ip] = {'MAC':mac,'TCP':[],'UDP':[]}
        if "|<TCP" in packet:
            dport_matches = dport.search(packet)
            if dport_matches:
                match = dport_matches.group()
                port = match.split('=')[1]
                if port not in ip_mac[ip]['TCP']:
                    if port != '':
                        ip_mac[ip]['TCP'].append(port)
        if "|<UDP" in packet:
            dport_matches = dport.search(packet)
            if dport_matches:
                match = dport_matches.group()
                port = match.split('=')[1]
                if port not in ip_mac[ip]['UDP']:
                    if port != '':
                        ip_mac[ip]['UDP'].append(port)
    ip_mac[ip]['TCP'].sort(reverse=True)
    ip_mac[ip]['UDP'].sort(reverse=True)
    return ip_mac

# This function will print all he IPs and its informaion
def everything():
    everything_from_source()
    everything_from_destination()

# This function is to print everything from the source
def everything_from_source():
    src_ip_count = set_src_ip()
    src = match_src_ip_mac_TCP_UDP()
    print("--------------------")
    print("| SOURCE DETAIL(s) |")
    print("--------------------")
    count = 1
    for k1, v1 in src.items():
        print("(" + str(count) + ") IP:", end=' ')
        print(k1, end='\t')
        for k2, v2 in v1.items():
            if k2 == 'MAC':
                print("\n     MAC:", end=' ')
                print(v2)
            if k2 == 'TCP':
                print("\t> TCP PORT(s):", end=' ')
                if v2 == []:
                    print('No port on this protocol')
                else:
                    for tport in v2:
                        print(tport, end=' ')
                    print()
            if k2 == 'UDP':
                print("\t> UDP PORT(s):", end=' ')
                if v2 == []:
                    print('No port on this protocol')
                else:
                    for uport in v2:
                        print(uport, end=' ')
                    print()
        if k1 in src_ip_count.keys():
            print("\t> IP COUNT:", end=' ')
            print(src_ip_count[k1])
            print()
        count += 1

# This function is to print everything from the destination
def everything_from_destination():
    dst_ip_count = set_dst_ip()
    dst = match_dst_ip_mac_TCP_UDP()
    print("-------------------------")
    print("| DESTINATION DETAIL(s) |")
    print("-------------------------")
    count = 1
    for k1, v1 in dst.items():
        print("(" + str(count) + ") IP:", end=' ')
        print(k1, end='\t')
        for k2, v2 in v1.items():
            if k2 == 'MAC':
                print("\n     MAC:", end=' ')
                print(v2)
            if k2 == 'TCP':
                print("\t> TCP PORT(s):", end=' ')
                if v2 == []:
                    print('No port on this protocol')
                else:
                    for tport in v2:
                        print(tport, end=' ')
                    print()
            if k2 == 'UDP':
                print("\t> UDP PORT(s):", end=' ')
                if v2 == []:
                    print('No port on this protocol')
                else:
                    for uport in v2:
                        print(uport, end=' ')
                    print()
        if k1 in dst_ip_count.keys():
            print("\t> IP COUNT:", end=' ')
            print(dst_ip_count[k1])
            print()
        count += 1

# -- #

# get all the ips and save it to a list, and then print it
def set_all_ip():
    dst_ip = set_dst_ip()
    src_ip = set_src_ip()
    all_ip = []
    for key in dst_ip.keys():
        all_ip.append((key))
    for key in src_ip.keys():
        if key not in all_ip:
            all_ip.append(key)
        else:
            continue
    return all_ip

# This function will print all the IP address found on a pcap file, that includes source and destination IP Addresses
def get_all_ip():
    count = 1
    ips = sorted(set_all_ip(), key=None, reverse=True)
    src_ip = set_src_ip()
    dst_ip = set_dst_ip()
    print("All the IP Addresses found in the PCAP file:")
    for ip in ips:
        if (ip in src_ip) and (ip in dst_ip):
            print(f"{count}. {ip} => {src_ip[ip] + dst_ip[ip]}")
        elif ip in src_ip:
            print(f"{count}. {ip} => {src_ip[ip]}")
        else:
            print(f"{count}. {ip} => {dst_ip[ip]}")
        count += 1

# This function will only print the Source IP addresses found in a pcap file
def get_all_src_ip():
    ips = set_src_ip()
    src_ip = []
    count = 1
    for key in ips.keys():
        src_ip.append(key)
    src_ip = sorted(src_ip, key=None, reverse=True)
    print("ALL THE SOURCE IP ADDRESSES AND THEIR COUNT AS A SOURCE IP")
    for ip in src_ip:
        print(f"{count}. {ip} => {ips[ip]}")
        count += 1

# This function will only print the Destination IP addresses found in a pcap file
def get_all_dst_ip():
    ips = set_dst_ip()
    dst_ip = []
    count = 1
    for key in ips.keys():
        dst_ip.append(key)
    dst_ip = sorted(dst_ip, key=None, reverse=True)
    print("ALL THE DESTINATION IP ADDRESSES AND THEIR COUNT AS A DESTINATION IP")
    for ip in dst_ip:
        print(f"{count}. {ip} => {ips[ip]}")
        count += 1

# This function will get all the source MAC addresses
def set_src_mac():
    dictionary = {}
    packet_output = read_file()
    src_mac = re.compile('src=([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')
    for packet in packet_output:
        src_matches = src_mac.search(packet)
        if src_matches:
            match1 = src_matches.group()
            # Do split the match string based on '=' as the delimiter
            mac = match1.split('=')[1]
            # If the ip is not in the dictionary then add 1 to it
            if mac not in dictionary:
                dictionary[mac] = 1
            # If the ip is in the dictionary then increment it
            else:
                dictionary[mac] += 1
    return dictionary

# This function will get all the destination MAC addresses
def set_dst_mac():
    dictionary = {}
    packet_output = read_file()
    dst_mac = re.compile('dst=([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')
    for packet in packet_output:
        dst_matches = dst_mac.search(packet)
        if dst_matches:
            match1 = dst_matches.group()
            # Do split the match string based on '=' as the delimiter
            mac = match1.split('=')[1]
            # If the ip is not in the dictionary then add 1 to it
            if mac not in dictionary:
                dictionary[mac] = 1
            # If the ip is in the dictionary then increment it
            else:
                dictionary[mac] += 1
    return dictionary

# This function will get all the source ip and their mac addresses
def match_src_ip_and_mac():
    ip_mac = {}
    packet_output = read_file()
    src_ip = re.compile('src=([0-9]{1,3}\.){3}[0-9]{1,3}')
    src_mac = re.compile('src=([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')
    for packet in packet_output:
        if "|<IP" in packet:
            ip_matches = src_ip.search(packet)
            mac_matches = src_mac.search(packet)
            if ip_matches and mac_matches:
                match1 = ip_matches.group()
                match2 = mac_matches.group()
                ip = match1.split('=')[1]
                mac = match2.split('=')[1]
                if ip not in ip_mac:
                    ip_mac[ip] = mac
                else:
                    pass
    return ip_mac

# This function will get all the destination ip and their mac addresses
def match_dst_ip_and_mac():
    ip_mac = {}
    packet_output = read_file()
    dst_ip = re.compile('dst=([0-9]{1,3}\.){3}[0-9]{1,3}')
    dst_mac = re.compile('dst=([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')
    for packet in packet_output:
        if "|<IP" in packet:
            ip_matches = dst_ip.search(packet)
            mac_matches = dst_mac.search(packet)
            if ip_matches and mac_matches:
                match1 = ip_matches.group()
                match2 = mac_matches.group()
                ip = match1.split('=')[1]
                mac = match2.split('=')[1]
                if ip not in ip_mac:
                    ip_mac[ip] = mac
                else:
                    pass
    return ip_mac

# This function will get all the TCP and UDP ports from the SOURCE IP
def source_ports():
    s_ports = {'TCP':[], 'UDP':[]}
    packet_output = read_file()
    sport = re.compile('sport=([0-9]{1,6}|[a-zA-Z]{1,25})')
    for packet in packet_output:
        if "|<TCP" in packet:
            sport_matches = sport.search(packet)
            if sport_matches:
                match = sport_matches.group()
                port = match.split('=')[1]
                if port not in s_ports['TCP']:
                    if port != '':
                        s_ports['TCP'].append(port)
        elif "|<UDP" in packet:
            sport_matches = sport.search(packet)
            if sport_matches:
                match = sport_matches.group()
                port = match.split('=')[1]
                if port not in s_ports['UDP']:
                    if port != '':
                        s_ports['UDP'].append(port)
    s_ports['TCP'].sort(reverse=True)
    s_ports['UDP'].sort(reverse=True)
    return s_ports

# This function will get all the TCP and UDP ports from the DESTINATION IP
def destination_ports():
    d_ports = {}
    d_ports['TCP'] = []
    d_ports['UDP'] = []
    packet_output = read_file()
    dport = re.compile('dport=([0-9]{0,6}|[a-zA-Z]{1-25})')
    for packet in packet_output:
        if "|<TCP" in packet:
            dport_matches = dport.search(packet)
            if dport_matches:
                match = dport_matches.group()
                port = match.split('=')[1]
                if port not in d_ports['TCP']:
                    if port != '':
                        d_ports['TCP'].append(port)
        elif "|<UDP" in packet:
            dport_matches = dport.search(packet)
            if dport_matches:
                match = dport_matches.group()
                port = match.split('=')[1]
                if port not in d_ports['UDP']:
                    if port != '':
                        d_ports['UDP'].append(port)
    d_ports['TCP'].sort(reverse=True)
    d_ports['UDP'].sort(reverse=True)
    return d_ports
