import socket
import threading
from tkinter import*
from tkinter import filedialog, messagebox #filedialog is used to open file selection dialogs..
#messagebox is used to show various types of message boxes (info, warning, error, etc.).

def upload_file():
    filename = filedialog.askopenfilename()#askopenfilename() in a Python tkinter application to select a file and then do something with that file, like display its path in the GUI:
    if filename:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 9999))
            client.send(f"UPLOAD {filename.split('/')[-1]}".encode())# Extracts the base name of the file from the full path.
            with open(filename, "rb") as f:# Opens the selected file in binary read mode ("rb").
                while (chunk := f.read(1024)): #Uses the walrus operator := to both assign the result of f.read(1024) to the variable chunk and evaluate it within the loop condition.
                    client.send(chunk)
            client.close()
            messagebox.showinfo("Success", f"{filename} uploaded.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")

def download_file():
    filename = entry.get()# you might use an Entry widget to allow the user to input a filename they wish to download or upload. When the user clicks a button (e.g., "Download File" or "Upload File"), the function tied to that button (download_file in the example) retrieves the filename from the Entry widget using entry.get().
    if filename:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 9999))
            client.send(f"DOWNLOAD {filename}".encode())
            with open(f"downloaded_{filename}", "wb") as f:
                while True:
                    bytes_read = client.recv(1024)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
            client.close()
            messagebox.showinfo("Success", f"{filename} downloaded.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download file: {e}")

# Setting up the GUI
root =Tk()
root.title("File Transfer System")
root.config(bg='lightblue')
root.geometry("600x600")

frame = Frame(root) #Creation: frame is created as a child of root
frame.pack(pady=20)
frame.config(bg='lightblue')

upload_button = Button(frame, text="Upload File", command=upload_file)
upload_button.pack(side=LEFT, padx=10)
upload_button.config(bg='blue')

entry = Entry(frame, width=40)
entry.pack(side=LEFT, padx=10)
entry.insert(0, "Enter filename to download")

download_button = Button(frame, text="Download File", command=download_file)
download_button.pack(side=LEFT, padx=10)
download_button.config(bg='#5e7cae')

root.mainloop()
