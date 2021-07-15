import pyshark
from First_Option import *
from scapy.all import *

file = read_sys_argv()  # returning a file
cap = pyshark.FileCapture(file)  # reading pcap
all_ips = {}
syn_count = 0
sus_packs = []
sus_http = []

def packet_data(cap):
    Cap = cap
    for packet in Cap:
        try:
            src = packet['ip'].src
            src_flag = packet['tcp'].flags
            dst = packet['ip'].dst
            dst_port = packet['tcp'].dstport
            numb = packet.number.show
            if src_flag == '0x00000002':
                if src not in all_ips:
                    all_ips[src] = {}
                    all_ips[src]['syn'] = 1
                    all_ips[src]['ports'] = []
                    all_ips[src]['packs'] = []
                    all_ips[src]['packs'].append(numb)
                    all_ips[src]['dst'] = []
                    all_ips[src]['dst'].append(dst)

                elif src in all_ips:
                    all_ips[src]['syn'] += 1
                    all_ips[src]['ports'].append(dst_port)
                    all_ips[src]['packs'].append(numb)
                    all_ips[src]['dst'].append(dst)
                else:
                    pass
            else:
                pass
        except:
            pass
    Cap.close()


def detect_ftp_brute_force():
    for ip in all_ips:
        ports = all_ips[ip]['ports']
        unique_list = []
        for x in ports:
            if x not in unique_list:
                unique_list.append(x)
        ftp_count = all_ips[ip]['ports'].count('21')
        victim_l = all_ips[ip]['dst']
        victim = max(victim_l, key=victim_l.count)
        if ftp_count > 4:
            print(f'{victim} was a victim of FTP BRUTE FORCE ATTACK')
            print("The attacker has failed to login {0} times".format(ftp_count))
            print(f"Possible Attacker: {ip}")

def detect_ssh_brute_force():
    #packet_data(cap)
    for ip in all_ips:
        ports = all_ips[ip]['ports']
        unique_list = []
        for x in ports:
            if x not in unique_list:
                unique_list.append(x)
        ssh_count = all_ips[ip]['ports'].count('22')
        victim_l = all_ips[ip]['dst']
        victim = max(victim_l, key=victim_l.count)
        if ssh_count > 4:
            print(f'{victim} was a victim of SSH BRUTE FORCE ATTACK')
            print("The attacker has failed to login {0} times".format(ssh_count))
            print(f"Possible Attacker: {ip}")

def detect_nmap_scan():
    for ip in all_ips:
        ports = all_ips[ip]['ports']
        unique_list = []

        for x in ports:
            if x not in unique_list:
                unique_list.append(x)
        uniq_p = len(all_ips[ip]['ports'])
        uniq_s = len(unique_list)
        victim_l = all_ips[ip]['dst']
        victim = max(victim_l, key=victim_l.count)
        if uniq_s > 100:
            print('ALERT: NMAP SCAN DETECTED')
            print("Potential Attacker: " + ip)
            print('{0} unique ports have been scanned'.format(uniq_p))
            pack_1 = all_ips[ip]['packs'][0]
            pack_2 = len(all_ips[ip]['packs']) - 1
            print('Suspicious Packets: {0} ==> {1}'.format(pack_1, pack_2))
            print('Possible Victim IP: {0}'.format(victim))
            ##### Nmap scan type processsor ########
            if uniq_s > 900:
                print("Nmap Scan Type: Top 1000")
            elif uniq_s > 500:
                print("Nmap Scan Type: Top 500")
            elif uniq_s >= 100:
                print("Nmap Scan Type: Top 100")
            else:
                print("NO NMAP")

def runit():
    packet_data(cap)
    detect_nmap_scan()
    detect_ssh_brute_force()
    print('')
    detect_ftp_brute_force()