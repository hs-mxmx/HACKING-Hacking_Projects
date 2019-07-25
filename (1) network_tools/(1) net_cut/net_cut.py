#!/usr/bin/env python

import netfilterqueue


def process_packet(packet):
    print(packet)
        #packet.accept()
        #packet.drop()


queue = netfilterqueue.NetfilterQueue()
#Bind to queue num and a call back function for trapped packets
queue.bind(0, process_packet)
queue.run()