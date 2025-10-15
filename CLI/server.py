import socket
import threading

HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050  
FORMAT = 'utf-8'
DISCONNECT_MSG = '^DISCONNECT!'
ASSIGN_MASTER_MSG = 'ROLE|MASTER'

print(f"server running on {HOST}:{PORT}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))


class Server:
    def __init__(self):
        self.clients = []
        self.client_info = {}
        self.master_event = threading.Event()  
        self.voting_round_active = threading.Event()
        self.lock = threading.Lock()
        self.votes = [0]
        self.responses = 0
        self.user_count = 0
        self.turn = 0
    
    @staticmethod
    def send_msg(conn,msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' '*(HEADER - len(send_length))

        conn.send(send_length)
        conn.send(message)


    def broadcast(self, message ,exclude = None):
        for user in self.clients:
            if user['conn'] != exclude:
                Server.send_msg(user['conn'],message)

    def vote(self,user):
            Server.send_msg(user['conn'],'Voting round is ongoing..')
            self.broadcast("PROMPT|VOTE|Enter Y/N based on if you want the current song to be played or not.")
            
            if self.votes>=self.user_count/2:
                self.broadcast(f"{user['song']} is being played now.")

            else:
                self.broadcast(f"Song has been dequeued")
            self.voting_round_active.clear()
            self.turn+=1

    def choose_song(self):
        print(len(self.clients))
        if len(self.clients)>1:
            user = self.clients[self.turn]
            current_conn = user['conn']
            Server.send_msg(current_conn,"PROMPT|SELECT| It's your turn to choose a song.")
            self.broadcast(f"{user['name']} is choosing...",exclude=user['conn'])       
            if self.voting_round_active.is_set():
                self.vote(user)

    @staticmethod
    def recv_exact(conn, length):
        data = b''
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data

    def handle_client(self,conn,addr):
        print(f'New connection {addr} connected ')
        connected = True

        for user in self.clients:
            if user['conn'] == conn:
                this_user = user        
        
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            # msg_length = self.recv(conn, HEADER).decode(FORMAT).strip()
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MSG:
                    if conn == self.clients[0]['conn'] and len(self.clients)>1:
                        first_client = self.clients[1]['conn']
                        Server.send_msg(first_client,'NOTICE|ROLE|You are the Admin.')
                    for client in self.clients:
                        if client.get('conn') == conn:
                            self.clients.remove(client)
                            break
                    connected = False
            
                if msg.startswith('RESPONSE|'):
                    type_ = msg.split("|")[1]
                    response = msg.split("|")[2]
                    if type_ == 'NAME':
                        this_user['name'] = response
                        print(self.clients)
                        Server.send_msg(conn,f'Hello {response} - Get ready to lock-in!')
                    elif type_ == 'SELECT':
                        this_user['song'] = response
                        self.voting_round_active.set()
                    elif type_=='VOTE':
                        this_user['vote'] = True
                        if self.votes==0:
                            self.user_count =len(self.clients)
                        if response == 'N':
                            self.votes+=1
                        
                if msg.startswith('CONFIRM|'):
                    self.master_event.set()                
                print(f'[{addr} sent {msg}]')

                
                if (len(self.clients) == 1 and not self.master_event.is_set()):
                    self.send_msg(conn,'NOTICE|ROLE|You are the Admin.')
            
                self.choose_song()
        conn.close()

    def start(self):
        server.listen()
        while True:
            # This line blocks until it receives conn,addr
            conn,addr = server.accept()
            client_info = {'conn': conn}

            # Before client_info was a shared global, now I'm making it a thread specific variable, so that no overwriting happens..
            # Basically, even if 2 users join at the same time, their information wouldn't be overwritten as each of them would have a copy of their own

            thread = threading.Thread(target=self.handle_client, args = (conn,addr))
            thread.start()

            # Bug Fixed: If .copy() isn't done, reference to dictionary gets overwritten everytime.
            with self.lock:    
                self.clients.append(client_info)

            Server.send_msg(conn,'PROMPT|NAME| Enter your username:')


if __name__ == "__main__":
    server_ = Server()
    server_.start()