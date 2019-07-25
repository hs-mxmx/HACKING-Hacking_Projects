#!/usr/bin/env python
#https://pythex.org -> Regex


import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Set new MAC address")
    (options, arguments) = parser.parse_args()
    # Allows the object to understand the values the user entered
    if not options.interface:
        #code to handle error
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        #code to handle error
        parser.error("[-] Please specify a MAC address, use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    # More Secure because the data is treated as a list together, avoiding hijacking
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def mac_changer():
    options = get_arguments()
    ifconfig_result = subprocess.check_output((["ifconfig", options.interface]))
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    #print(ifconfig_result)
    #print(mac_address_search_result.group(0))

    if mac_address_search_result:
        if mac_address_search_result.group(0) == options.new_mac:
            print("[-] The MAC address you have entered, is already set")
        else:
            change_mac(options.interface, options.new_mac)
    else:
        print("[-] Could not read MAC address")


mac_changer()


# interface = options.interface
# new_mac = options.new_mac

# For Python3
# interface = input("interface > ")
# new_mac = input("new MAC > ")

# subprocess.call("ifconfig " + interface + " down", shell=True)
# subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
# subprocess.call("ifconfig " + interface + " up" , shell=True)


# Functions
# options = get_arguments()
# change_mac(options.interface, options.new_mac)


# ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
# print(ifconfig_result)
