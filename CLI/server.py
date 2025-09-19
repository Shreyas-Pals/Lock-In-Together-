import socket
import threading

HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050  
FORMAT = 'utf-8'
DISCONNECT_MSG = '^DISCONNECT!'

print(f"Server running on {HOST}:{PORT}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

def handle_client(conn,addr):
    print('New connection {addr} connected ')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            print(f'[{addr} sent {msg}]')
        
    conn.close()

def start():
    server.listen()
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args = (conn,addr))
        thread.start()
        print(f'Active connections:{threading.active_count()-1}')

print('Server is starting')
start()
