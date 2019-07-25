# -1-Hacking_Projects
Python Hacking Projects (Network Scanner, Mac Changer, Sniffers, ARP Spoofing, Backdoor, Keyloggers...)

# [1] Network_Tools 
Contains several tools and programs to scan, attack and detect dangerous variations on the network.
- ARP_Spoofing: Allows to perform an attack (MitM) on a local Network, ([+] Needs to Set up IPtables)
    -> iptables -I OUTPUT -j NFQUEUE --queue-num 0  (0 is set by me on code)
    -> iptables -I INPUT -j NFQUEUE --queue-num 0  
- ARP_Spoof_Detector: Allows to detect and scan the packets send and recieved in case we are getting hijacked
- DNS_Spoof (Test): Allows to spoof the DNS to redirect the current target to another ip/website
- Net_Cut: Test for another projects
- Network_Scanner: Allows to send a broadcast request to get the current online machines/hosts, and get their ip/mac.
- Sniffer: Performs as a listener on the network where the packets are sent, ([+] Needs ARP_Spoofing)

# [2] Mac Changer
Simple programs that allows you to change your current MAC Address 

# [3] Remote_netshell
Interesting programs based in hijacking and remote attacks.
- Backdoor: Performs a backdoor attack allowing you to upload, download, send, and recieve files, packets... via local/host service.
- Code_Injector: Allows to perform a Js injection in http pages or unprotected to attack the current target for hijacking, beef and exploits, ([+] Needs ARP_Spoofing, SSlstrip, Iptables)
    -> iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
    -> iptables flush to clear current iptables
- Download_Execute: Allows to perform an execute attack after download, injected in the background code (Test with jpg, png files)
- Download_Execute_And_Report: Same as the previous one, but sends a smtp request with the data to your gmail account.
- Execute_And_Report: Same as the previous one but without the Download Option, (Test project)
- Download_File_Malware: Test set to clone a download link into a file
- Execute Command: Allows to execute OS commands via python, (Test project)
- Keylogger: Structured program based in keylogger attack, recording the keys and sending the current results every (?) minutes to your gmail account.
- Keylogger_Without_Email: Same as the previous one but without sending any email, (Test project)
- Local-Server-Host: Performs a Server/Host connection.
- Replace Download: Allows to change the download file from the target computer, ([+] Needs ARP_Spoofing, IPtables)

# [4] Hacking_and_Scanners
Tools that perform scanners and tests for vulnerabilities and exploits to webapps.
- Brute Dictionary: Performs a Test repetition for current username and password on the target website
- Crawler: Structured program that can get the subdomains and hidden subdomains from a website, ([+] Requires txt files, see on code)
- Extract Form: Program that extracts the forms from a current website via Page Source Code.
- Spider: Program that extracts all the links that can be found in Page Source Code (recursively)
- Vulnerability Scanner: Mix formed by previous programs to scan and test the websites we can found trough a domain, includes XSS simple test to perform testing and scanner (XSS_stored and XSS_based)
