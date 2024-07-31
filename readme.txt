This project is a simple socket-based chat application that allows multiple clients to connect
to a server and communicate with each other in real-time.
 It includes basic user authentication before joining the chat.

Features
Real-time chat with multiple clients
User authentication before joining the chat
Graphical User Interface (GUI) for the client using Tkinter
Requirements
Python 3.x
Tkinter (usually included with Python)
A local network connection
How to Run
Server
Open a terminal or command prompt.
Navigate to the directory containing the server.py file.
Run the server using the following command:
bash
Copy code
python server.py
Client
Open a terminal or command prompt.
Navigate to the directory containing the client.py file.
Run the client using the following command:
bash
Copy code
python client.py
Enter the username and password to authenticate and join the chat. Use the credentials defined in the server (e.g., user1,password1).
File Structure
server.py: The server script that handles client connections, authentication, and message broadcasting.
client.py: The client script that provides a GUI for users to enter their credentials and chat.
How it Works
Server
The server listens for incoming client connections on a specified IP address and port.
It maintains a dictionary of valid usernames and passwords for authentication.
When a client connects, the server receives the credentials and checks them against the dictionary.
If authentication is successful, the client is allowed to join the chat. Otherwise, the connection is closed.
The server broadcasts messages from any client to all other connected clients.
Client
The client connects to the server using the specified IP address and port.
It prompts the user to enter a username and password for authentication.
If authentication is successful, the client displays the chat interface.
Users can send messages, which are then broadcasted to all other clients by the server.
Example Credentials
The server script (server.py) includes a dictionary of valid usernames and passwords.
 For testing purposes, you can use the following credentials:

Username: user1
Password: password1

Acknowledgements
The project uses the Tkinter library for the client GUI.
Socket programming is used for network communication between the server and clients.