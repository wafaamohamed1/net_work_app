import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Server settings
HOST = '127.0.0.1'
PORT = 7000

class ChatServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Server")

        # Create GUI elements
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', width=80, height=20, bg='#1D2D50', fg='#E0E0E0')
        self.chat_area.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=60, bg='#2E3A59', fg='#E0E0E0')
        self.message_entry.pack(padx=10, pady=(0, 10), side=tk.LEFT)

        self.send_button = tk.Button(root, text="Send", command=self.send_message, bg='#6A0D91', fg='#E0E0E0')
        self.send_button.pack(pady=(0, 10), side=tk.LEFT)

        # Initialize socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen()

        self.clients = []
        self.nicknames = []

        # Start receiving messages
        threading.Thread(target=self.receive_connections, daemon=True).start()

    def broadcast(self, message):
        """Send a message to all connected clients."""
        for client in self.clients:
            try:
                client.send(message)
            except:
                client.close()
                self.clients.remove(client)

    def handle_client(self, client):
        """Handle communication with a specific client."""
        while True:
            try:
                message = client.recv(1024)
                if not message:
                    break
                nickname = self.nicknames[self.clients.index(client)]
                self.display_message(f"{nickname} says: {message.decode('utf-8')}")
                self.broadcast(message)  
            except Exception as e:
                print(f"Error: {e}")
                break
    
        # Cleanup after client disconnects
        index = self.clients.index(client)
        self.clients.remove(client)
        client.close()
        nickname = self.nicknames.pop(index)
        self.broadcast(f"{nickname} has left the chat.".encode('utf-8'))
        self.display_message(f"{nickname} has left the chat.")

    def receive_connections(self):
        """Accept new client connections and handle them."""
        while True:
            client, address = self.server.accept()
            self.display_message(f"Connected with {str(address)}")
            
            client.send("Nickname".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            if nickname:
                self.nicknames.append(nickname)
                self.clients.append(client)
            
                self.broadcast(f"{nickname} has joined the chat.".encode('utf-8'))
                self.display_message(f"{nickname} has joined the chat.")
                threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def send_message(self):
        """Send a message to all clients."""
        message = self.message_entry.get()
        if message:
            self.broadcast(message.encode('utf-8'))
            self.display_message(f"Server: {message}")
            self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        """Display a message in the chat area."""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatServerGUI(root)
    root.mainloop()
