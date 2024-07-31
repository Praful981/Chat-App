import socket
import threading

class ChatServer:
    def __init__(self):
        self.clients_list = []
        self.server_socket = None
        self.users = {"ataln": "abc@123", "prafuln": "abc@123"}  # Dictionary of valid usernames and passwords
        self.create_listening_server()

    def create_listening_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_ip = '127.0.0.1'
        local_port = 10319
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming messages..")
        self.server_socket.listen(5)
        self.receive_messages_in_a_new_thread()

    def receive_messages(self, so):
        while True:
            try:
                incoming_buffer = so.recv(256)
                if not incoming_buffer:
                    break
                self.broadcast_to_all_clients(so, incoming_buffer.decode('utf-8'))
            except ConnectionResetError:
                break
        self.remove_client(so)
        so.close()

    def broadcast_to_all_clients(self, senders_socket, message):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket != senders_socket:
                try:
                    socket.sendall(message.encode('utf-8'))
                except BrokenPipeError:
                    self.remove_client(socket)

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            print(f"Connection from {ip}:{port}")
            if self.authenticate_client(so):
                self.add_to_clients_list(client)
                print('Connected to ', ip, ':', str(port))
                t = threading.Thread(target=self.receive_messages, args=(so,))
                t.start()
            else:
                print(f"Authentication failed for {ip}:{port}")

    def authenticate_client(self, client_socket):
        try:
            credentials = client_socket.recv(256).decode('utf-8')
            username, password = credentials.split(',')
            if self.users.get(username) == password:
                client_socket.send("SUCCESS".encode('utf-8'))
                return True
            else:
                client_socket.send("FAILURE".encode('utf-8'))
                client_socket.close()
                return False
        except Exception as e:
            print(f"Error during authentication: {e}")
            client_socket.close()
            return False

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)

    def remove_client(self, client_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket == client_socket:
                self.clients_list.remove(client)
                break

if __name__ == "__main__":
    ChatServer()
