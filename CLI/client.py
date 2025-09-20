import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = '^DISCONNECT!'
SERVER = '172.16.140.82'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER,PORT))
master_role =  False
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    send_length += b' '*(HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

def listen():
    while True:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            split_ = msg.split("|")
            if len(split_)>2:
                type,message = split_[1], split_[2]
        
        '''
        MESSAGE TYPES:-
        '''

        if msg.startswith('NOTICE|'):
            print(f'[{split_[0]}] {message}')
            if type == 'ROLE':
                global master_role
                master_role = True
                send('CONFIRM|ROLE')

        elif msg.startswith('PROMPT|'):
            name = input(f'[{split_[0]}]{message} ')

            if type == 'NAME':
                send(f"RESPONSE|{type}|{name}")

        # send(DISCONNECT_MSG)
        else:
            print(f'[SERVER]:{msg}')
thread = threading.Thread(target=listen)
thread.start()
thread.join()
# client.close()


    # send('Hello World!')

# send(DISCONNECT_MSG)