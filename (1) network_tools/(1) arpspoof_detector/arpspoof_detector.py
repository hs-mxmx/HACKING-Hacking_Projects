#!/usr/bin/env python

#!/usr/bin/env python

import optparse
import scapy.all as scapy
import sys
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[1]
    # print(unanswered_list)

    return answer_list[0][1].hwsrc


def scan(packet):
    arp_request = scapy.ARP(pdst="192.168.1.0/24")
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    #arp_request_broadcast.show() -> Display the content [ARP / Ethernet]
    answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[1]
    attacker_list = []
    for element in answer_list:
        if element[1].hwsrc == packet.hwsrc:
            attacker_list.append(element[1].psrc)
        #print("\t" + element[1].psrc + "\t\t" + element[1].hwsrc)
    return attacker_list


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                attacker = scan(packet)
                print("\n\r[+] You are getting spoofed, please QUIT!")
                print(" Gateway: " + "(" + packet[scapy.ARP].psrc)  + ")  " + "(" + real_mac + ")"
                print(" Attacker: " + "(" + attacker[0] + ") " + "(" + response_mac + ")")


        except IndexError:
            pass


sniff("wlan0")

