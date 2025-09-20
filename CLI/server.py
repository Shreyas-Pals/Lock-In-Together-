import socket
import threading

HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050  
FORMAT = 'utf-8'
DISCONNECT_MSG = '^DISCONNECT!'
ASSIGN_MASTER_MSG = 'ROLE|MASTER'

print(f"Server running on {HOST}:{PORT}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

# List of all clients' infos
clients = []
# Info belonging to a single client
client_info = {}
master_event = threading.Event()  


def send_msg(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))

    conn.send(send_length)
    conn.send(message)



def handle_client(conn,addr):
    print(f'New connection {addr} connected ')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                if conn == clients[0]['conn']:
                    master_event.clear()
                clients.remove(client_info)
                connected = False
                
            if msg.startswith('RESPONSE|'):
                response = msg.split("|")[2]
                client_info['name'] = response
                send_msg(conn,f'Hello {response} - Get ready to lock-in!')
            
            if msg.startswith('CONFIRM|'):
                master_event.set()
                
            print(f'[{addr} sent {msg}]')
        
    conn.close()

def start():
    server.listen()
    while True:
        conn,addr = server.accept()
        client_info['conn'] = conn

        thread = threading.Thread(target=handle_client, args = (conn,addr))
        thread.start()

        clients.append(client_info)
        if not master_event.is_set(): 
            first_client = clients[0]['conn']
            send_msg(first_client,'NOTICE|ROLE|You are the Admin.')

        send_msg(conn,'PROMPT|NAME| Enter your username:')
        # print(f'Active connections:{threading.active_count()-1}')

# print('Server is starting')

if __name__ == "__main__":
    start()