import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog
import os

# Client settings
HOST = '127.0.0.1'
PORT = 7000

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        # Apply space theme colors
        self.bg_color = '#000000'  # Deep black
        self.chat_bg_color = '#1D2D50'  # Dark blue
        self.text_color = '#E0E0E0'  # Light gray
        self.button_color = '#6A0D91'  # Purple
        self.entry_color = '#2E3A59'  # Darker blue

        # Create chat area
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20,
                                                  bg=self.chat_bg_color, fg=self.text_color, insertbackground='white')
        self.chat_area.pack(padx=10, pady=10)

        # Create message entry
        self.message_entry = tk.Entry(root, width=60, bg=self.entry_color, fg=self.text_color, insertbackground='white')
        self.message_entry.pack(padx=10, pady=(0, 10), side=tk.LEFT)

        # Create send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message, bg=self.button_color, fg=self.text_color)
        self.send_button.pack(pady=(0, 10), side=tk.LEFT)

        # Create file button
        self.file_button = tk.Button(root, text="Send File", command=self.send_file, bg=self.button_color, fg=self.text_color)
        self.file_button.pack(pady=(0, 10), side=tk.LEFT)

        # Initialize socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        # Start receiving messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, f"You: {message}\n")
            self.chat_area.config(state='disabled')
            self.chat_area.yview(tk.END)

    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            filename = os.path.basename(file_path)
            self.client_socket.send(f"FILE:{filename}".encode('utf-8'))
            try:
                with open(file_path, 'rb') as file:
                    while chunk := file.read(1024):
                        self.client_socket.send(chunk)
                self.client_socket.send(b'--END--')  # Mark end of file
                self.chat_area.config(state='normal')
                self.chat_area.insert(tk.END, f"Sent file: {filename}\n")
                self.chat_area.config(state='disabled')
                self.chat_area.yview(tk.END)
            except Exception as e:
                self.chat_area.config(state='normal')
                self.chat_area.insert(tk.END, f"Error sending file: {e}\n")
                self.chat_area.config(state='disabled')
                self.chat_area.yview(tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message.startswith("FILE:"):
                    filename = message[5:]
                    with open(filename, 'wb') as file:
                        while True:
                            chunk = self.client_socket.recv(1024)
                            if chunk == b'--END--':
                                break
                            file.write(chunk)
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, f"Received file: {filename}\n")
                    self.chat_area.config(state='disabled')
                    self.chat_area.yview(tk.END)
                else:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, f"Server: {message}\n")
                    self.chat_area.config(state='disabled')
                    self.chat_area.yview(tk.END)
            except ConnectionResetError:
                break
            except Exception as e:
                self.chat_area.config(state='normal')
                self.chat_area.insert(tk.END, f"Error receiving message: {e}\n")
                self.chat_area.config(state='disabled')
                self.chat_area.yview(tk.END)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
