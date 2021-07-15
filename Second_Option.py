from scapy.all import *

import sys
pcap = rdpcap(sys.argv[1])
decoded_list = []

method = ['GET', 'POST', 'PUT','MGET','STOR']
k = []
s = {}
regex = re.compile('.*\.(jpg|JPG|gif|GIF|jpeg|php|pdf|txt)')

def extractfiles():
    for pkt in pcap:
        if Raw in pkt:
            p = repr(pkt[Raw])
            decoded_list.append(p)

    for line in decoded_list:
        matches = regex.search(line)
        if matches:
            match1 = matches.group()
            if match1 not in k:
                k.append(match1.split())
            else:
                pass
    for l in k:
        for x in l:
            matches = regex.search(x)
            if matches:
                match1 = matches.group()
                if '\\' in match1:
                    j = match1.split('\\')
                    match1 = j[-1]
                    if match1 not in s:
                        s[match1] = 1
                    else:
                        s[match1] += 1
                elif '/' in match1:
                    j = match1.split('/')
                    match1 = j[-1]
                    if match1 not in s:
                        s[match1] = 1
                    else:
                        s[match1] += 1
                elif "load='" in match1:
                    j = match1.split("'")
                    match1 = j[-1]
                    if match1 not in s:
                        s[match1] = 1
                    else:
                        s[match1] += 1
                else:
                    if match1 not in s:
                        s[match1] = 1
                    else:
                        s[match1] += 1
    print('Found these image and executable files in the pcap:')
    print('Name - Occurences')
    for k,v in s.items():
        print(k,'-',v)
    print("There are about " + str(len(s)) + " images and executable in this pcap file.")