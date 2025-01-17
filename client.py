from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox
import socket
import threading


class GUI:
    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.username_widget = None
        self.password_widget = None
        self.client_socket = None
        self.initialize_socket()
        self.initialize_gui()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = '127.0.0.1'
        remote_port = 10319
        self.client_socket.connect((remote_ip, remote_port))

    def initialize_gui(self):
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.display_authentication_section()

    def display_authentication_section(self):
        frame = Frame()
        Label(frame, text='Username:', font=("arial", 13, "bold")).pack(side='left', pady=20)
        self.username_widget = Entry(frame, width=60, font=("arial", 13))
        self.username_widget.pack(side='left', anchor='e', pady=15)
        Label(frame, text='Password:', font=("arial", 13, "bold")).pack(side='left', pady=20)
        self.password_widget = Entry(frame, width=60, font=("arial", 13), show='*')
        self.password_widget.pack(side='left', anchor='e', pady=15)
        self.join_button = Button(frame, text="Join", width=10, command=self.on_join).pack(side='right', padx=5, pady=15)
        frame.pack(side='top', anchor='nw')

    def display_chat_section(self):
        self.display_name_section()
        self.display_chat_entry_box()
        self.display_chat_box()
        self.listen_for_incoming_messages_in_a_thread()

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        thread.start()

    def receive_message_from_server(self, so):
        while True:
            try:
                buffer = so.recv(256)
                if not buffer:
                    break
                message = buffer.decode('utf-8')
                self.display_message(message)
            except OSError:
                break
        so.close()

    def display_message(self, message):
        self.chat_transcript_area.insert('end', message + '\n')
        self.chat_transcript_area.yview(END)

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Enter Your Name Here! ', font=("arial", 13, "bold")).pack(side='left', pady=20)
        self.name_widget = Entry(frame, width=60, font=("arial", 13))
        self.name_widget.pack(side='left', anchor='e', pady=15)
        frame.pack(side='top', anchor='nw')

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Chat Box', font=("arial", 12, "bold")).pack(side='top', padx=270)
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("arial", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=15, pady=10)
        scrollbar.pack(side='right', fill='y', padx=1)
        frame.pack(side='left')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter Your Message Here!', font=("arial", 12, "bold")).pack(side='top', anchor='w', padx=120)
        self.enter_text_widget = Text(frame, width=50, height=10, font=("arial", 12))
        self.enter_text_widget.pack(side='left', pady=10, padx=10)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='left')

    def on_join(self):
        if len(self.username_widget.get()) == 0 or len(self.password_widget.get()) == 0:
            messagebox.showerror("Enter your username and password", "Both fields are required")
            return
        self.client_socket.send((self.username_widget.get() + ',' + self.password_widget.get()).encode('utf-8'))
        response = self.client_socket.recv(256).decode('utf-8')
        if response == "SUCCESS":
            self.display_chat_section()
        else:
            messagebox.showerror("Authentication Failed", "Invalid username or password")
            self.client_socket.close()

    def on_enter_key_pressed(self, event):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        senders_name = self.name_widget.get().strip() + ": "
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (senders_name + data).encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)


if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
