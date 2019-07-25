#!/usr/bin/env python

import scapy.all as scapy
import optparse
#import argparse
#pip install scapy-python3 [pip install "module"] to install python modules in python3


def get_arguments():
    parser = optparse.OptionParser()
    #parser = argparse.ArgumentParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    #parser.add_argument()
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify a target, use --help for more info." +
                     "\nExample: > ./network_scanner.py -t 192.168.1.0/24 " +
                     "\nExample: > ./network_scanner.py --target 192.168.1.1/24 ")
    #(options) = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    #arp_request_broadcast.show() -> Display the content [ARP / Ethernet]
    answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[1]
    clients_list = []
    for element in answer_list:
        client_dict = {"IP": element[1].psrc,"MAC": element[1].hwsrc}
        clients_list.append(client_dict)
        #print("\t" + element[1].psrc + "\t\t" + element[1].hwsrc)
    return clients_list


def print_result(results_list):
    print("-----------------------------------------------------------------")
    print("\t    IP\t\t\t   MAC ADDRESS\n-----------------------------------------------------------------")
    for client in results_list:
        print("\t" + client["IP"] + "\t\t" + client["MAC"])


options = get_arguments()
print_result(scan(options.target))

#   scapy.ls(scapy.ARP()) [To Display Whats Inside]
#   scapy.arping(ip) || scapy.ls(scapy.Ether()) [To Make an ARP trough the whole network] ip = "192.168.1.0/24"
#   Create ethernet frame to be sent trough the whole network [IP & MAC addresses]
#   print(broadcast.summary())
#   print(arp_request.summary())
#   print(arp_request_broadcast.summary())

#   scapy.srp(arp_request_broadcast) [srp let send and recieve packets with modificate parts] instead of sr function
#   scapy.srp will return a couple of two lists, the first a list of couple(packet sent,answer)
#   and the second will be the unanswered packets, these two elements are lists but they are wrapped by an object
#   to represent them better

#   answer_list,unanswered_list = scapy.srp(arp_request_broadcast, timeout=1)

#   print(unanswered.summary())
#   print(answer_list.summary())

