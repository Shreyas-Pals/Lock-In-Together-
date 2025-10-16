import socket
import threading,time
from itertools import cycle

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
        self.master_exists = threading.Event()  
        self.voting_round_start = threading.Event()
        self.lock = threading.Lock()
        self.votes = 0
        self.responses = 0
        self.user_count = 0
        self.turn = 0
        self.block = threading.Event()
        self.queue = set()
    
    @staticmethod
    def send_msg(conn,msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' '*(HEADER - len(send_length))

        conn.send(send_length)
        conn.send(message)


    def broadcast(self, msg ,exclude = None):
        for user in self.clients:
            if user['conn'] != exclude:
                Server.send_msg(user['conn'],msg)

    def add_to_msg_queue(self,fnc,*args,**kwargs):
        message = kwargs.get('msg')
        if message not in self.queue:
            self.queue.add(message)
            fnc(*args,**kwargs)

    def vote(self,user):
            
            self.add_to_msg_queue(Server.send_msg,user['conn'],msg = "PROMPT|SELECT| It's your turn to choose a song.")
            self.add_to_msg_queue(self.broadcast,msg = f"{user['name']} is choosing...",exclude=user['conn'])
            self.add_to_msg_queue(Server.send_msg,user['conn'],msg = 'Voting round is ongoing..' )

            if self.voting_round_start.is_set():    
                self.add_to_msg_queue(self.broadcast,msg = f"PROMPT|VOTE|Enter N if you don't want {user['song']} to be played.",exclude = user['conn'])

                if self.votes>self.user_count/2:
                    self.add_to_msg_queue(self.broadcast,msg = f"{user['song']} has been dequeued")
                else:
                    self.add_to_msg_queue(self.broadcast,msg =f"{user['song']} is being played now.")
                    
                    # Reset for next round.
                self.voting_round_start.clear()
                self.votes = 0

                if self.turn >= len(self.clients)-1:
                    self.turn == 0
                else:
                    self.turn+=1
                
                self.queue.clear()


    def song_select(self):
        # current_voting_round_pending = threading.Event()
        while True:
            # ready_clients = [user for user in self.clients if user['name']]
            number_of_clients_who_are_ready = sum(1 for user in self.clients if user['name'] is not None)
            if number_of_clients_who_are_ready>1:
                user = self.clients[self.turn]   
                self.vote(user)

            time.sleep(3)


    def handle_client(self,conn,addr):
        print(f'New connection {addr} connected ')
        connected = True
        # For first user:-
        if not self.master_exists.is_set():
            master_conn = conn

        for user in self.clients:
            if user['conn'] == conn:
                this_user = user        
        
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MSG:
                    if this_user['master']==True and len(self.clients)>1:
                        self.clients.remove(this_user)
                        self.master_exists.clear()
                        master_conn = self.clients[0]['conn']
                    connected = False
            
                if msg.startswith('RESPONSE|'):
                    type_ = msg.split("|")[1]
                    response = msg.split("|")[2]
                    if type_ == 'NAME':
                        this_user['name'] = response
                        Server.send_msg(conn,f'Hello {response} - Get ready to lock-in!')
                    elif type_ == 'SELECT':
                        this_user['song'] = response       
                        #To get number of people just before voting round:-   
                        self.user_count =len(self.clients) 
                        self.voting_round_start.set()
                    elif type_=='VOTE':
                        this_user['vote'] = True                                 
                        if response == 'N':
                            self.votes+=1
                        
                if msg.startswith('CONFIRM|'):
                    self.master_exists.set()
                    this_user['master'] = True                
                print(f'[{addr} sent {msg}]')

                if not self.master_exists.is_set():
                    self.send_msg(master_conn,'NOTICE|ROLE|You are the Admin.')
        conn.close()

    def start(self):
        server.listen()
        while True:
            # This line blocks until it receives conn,addr
            conn,addr = server.accept()
            client_info = {'conn': conn,'master': False,'name':None}

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
    threading.Thread(target=server_.song_select, daemon=True).start()
    server_.start()
