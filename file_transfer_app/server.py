import socket
import threading
import os #The os module in Python is a standard utility module that provides a way to interact with the operating system. It includes functions for creating and removing a directory (folder), fetching its contents, managing paths,

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    if request.startswith("UPLOAD"):
        filename = request.split()[1] #is typically used in the context of handling HTTP requests or any similar input where the request string contains multiple parts that can be separated by spaces.
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(1024)
                if not bytes_read:
                    break
                f.write(bytes_read)
        print(f"{filename} uploaded successfully.")
    elif request.startswith("DOWNLOAD"):
        filename = request.split()[1]
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                while (chunk := f.read(1024)):
                    client_socket.send(chunk)
        else:
            client_socket.send(b"ERROR: File not found.")
        print(f"{filename} downloaded successfully.")
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999...")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
