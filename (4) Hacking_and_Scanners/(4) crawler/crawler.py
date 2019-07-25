
import requests, os, progressbar, optparse
from time import sleep


def get_options():
    parser = optparse.OptionParser()
    parser.add_option("-s", "--subdomains", dest="Subdomains", help="Search for website's subdomains"
                                                                     "\nSpecify 'H' or 'S'"
                                                                     "\n  S: Subdomains"
                                                                     "\nH: Hidden Subdomains")
    (options, arguments) = parser.parse_args()
    if not options.Subdomains:
        parser.error("[-] Please, specify one search option.")
    if options.Subdomains.upper() == "S" or options.Subdomains.upper() == "H":
        return options
    else:
        get_options()


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


def get_domains(url):
    options = get_options()
    try:
        total = 0
        total_2 = 0
        # Get Domains
        if options.Subdomains.upper() == "S":
            with open("/root/Desktop/crawler/subdomains.list", "r") as wordlist_file:
                print("\n\n\t\t\t   Loading Subdomain List")
                get_percentage()
                for line in wordlist_file:
                    word = line.strip()
                    test_url = word + "." + url
                    response = request(test_url)
                    if response:
                        total = total + 1
                        print("[" + str(total) + "] Subdomain Discovered -> " + test_url)
                        with open("/root/Desktop/crawler/subdomains.txt", "a") as avaliable_domains:
                            avaliable_domains.write(test_url + "\n")
        if options.Subdomains.upper() == "H":
            # Hidden Domains
            with open("/root/Desktop/crawler/hiddendomains.list", "r") as hidden_subdomains:
                print("\n\t\t\t   Loading Hidden Subdomain List")
                get_percentage()
                for line_2 in hidden_subdomains:
                    word_2 = line_2.strip()
                    test_url_2 = url + "/" + word_2
                    response_2 = request(test_url_2)
                    if response_2:
                        total_2 = total_2 + 1
                        print("[" + str(total_2) + "] Hidden Subdomains Discovered -> " + test_url_2)
                        with open("/root/Desktop/crawler/hiddendomains.txt", "a") as avaliable_subdomains:
                            avaliable_subdomains.write(test_url_2 + "\n")

        os.system("clear")
        print("\nTotal Subdomains: " + str(total))
        print("Total Hidden Subdomains: " + str(total_2))
    except KeyboardInterrupt:
        os.system("clear")
        print("[-]Quitting...")
        print("\nTotal Subdomains: " + str(total))
        print("Total Hidden Subdomains : " + str(total_2))


# def get_lines(file):
#    count = 0
#    thefile = open(file, "rb")
#    while 1:
#        buffer = thefile.read(8192*1024)
#        if not buffer:
#            break
#        count += buffer.count('\n')
#    thefile.close()
#    return count


def get_percentage():
    bar = progressbar.ProgressBar(maxval=20, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in xrange(20):
        bar.update(i+1)
        sleep(0.1)
    bar.finish()


target_url = "website/ip"
get_domains(target_url)

