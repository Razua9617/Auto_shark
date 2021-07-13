from scapy.all import *
import re
import sys

# Read the pcap file, loop over it and save it to a list
def read_file():
    file = sys.argv[1]
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
                if ip not in ip_mac:
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