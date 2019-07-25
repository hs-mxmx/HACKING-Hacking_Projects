
import listener, optparse, subprocess, re

def get_arguments():
        parser = optparse.OptionParser()
        parser.add_option("-p", "--port", dest="port", help="Specify local port")
        (options, arguments) = parser.parse_args()
        if not options.port:
            parser.error("[-] Please specify a port number using -p or --port (Not common recommended)")
        return options

def get_ip():
        ifconfig_result = subprocess.check_output((["ifconfig", "wlan0"]))
        ip_address_search_result = re.search(r"inet \w\w\w.\w\w\w.\w.{1,4}", ifconfig_result)
        get_local_ip = ip_address_search_result.group(0)
        get_local_ip = get_local_ip[5:]
        # print(get_local_ip)
        return get_local_ip


options = get_arguments()
ip = get_ip()
port = int(options.port)
my_listener = listener.Listener(ip, port)
my_listener.run()

