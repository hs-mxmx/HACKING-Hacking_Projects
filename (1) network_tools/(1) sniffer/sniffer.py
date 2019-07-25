#!/usr/bin/env python

import optparse
import scapy.all as scapy
from scapy.layers import http


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-v", "--VERSION", dest="show", help="Specify The print Version")
    parser.add_option("-i", "--INTERFACE", dest="interface", help="Specify Interface")
    (options, arguments) = parser.parse_args()
    if not options.show:
        parser.error("[-] Please specify an option: "
                     "\n -i [wlan0] -v [a] or -v [ALL] fully display of information"
                     "\n -i [eth0] -v [p] or -v [PWD] to display information about login"
                     "\n -i [lo] -v [h] or -v [HTTP] to display http requests' information"
                     "\n[*]Example: -i wlan0 -v a")
    if not options.interface:
        parser.error("[-] Please specify the Interface")
    return options


def sniff():
    opts = get_arguments()
    if opts.show == "a" or opts.show == "ALL":
        scapy.sniff(iface=opts.interface, store=False, prn=process_sniffed_packet_all)
    if opts.show == "p" or opts.show == "PWD":
        scapy.sniff(iface=opts.interface, store=False, prn=process_sniffed_packet_password)
    if opts.show == "h" or opts.show == "HTTP":
        scapy.sniff(iface=opts.interface, store=False, prn=process_sniffed_packet_http)

    #filter="udp","tcp","arp","port 80", "port 21"...


def process_sniffed_packet_password(packet):
    if packet.haslayer(http.HTTPRequest):
        get_url(packet)
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords = ["username", "login", "email", "user", "password", "pass", "passwd"]
            for keyword in keywords:
                if keyword in load:
                    print(load)
                    break


def get_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    print(url)


def process_sniffed_packet_http(packet):
    if packet.haslayer(http.HTTPRequest):
        print("\n### HTTP ###\n")
        print(packet[3])
        print("\n### HTTP REQUEST ###\n")
        print(packet[4])


def process_sniffed_packet_all(packet):
    print(packet.show())


sniff()


#def http_header(packet):
#   http_packet=str(packet)
#   if http_packet.find('GET'):
#       return GET_print(packet)


