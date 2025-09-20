import socket
import threading
import time,sys
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = '^DISCONNECT!'
SERVER = '172.16.140.82'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER,PORT))
master_role =  threading.Event()

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

        #  Did this to remove a bug which was sending [SERVER] message
        #  even after it's disconnected, it turned out to be because of
        #  the EOF protocol which sends empty bytes which were being received
        #  by recv, so this breaks loop when im receiving empty bytes which signifies
        #  end of code.
        else:
            break
        
        '''
        MESSAGE TYPES:-
        '''

        if msg.startswith('NOTICE|'):
            print(f'[{split_[0]}] {message}')
            if type == 'ROLE':
                master_role.set()
                send('CONFIRM|ROLE')

        elif msg.startswith('PROMPT|'):
            name = input(f'[{split_[0]}]{message} ')

            if type == 'NAME':
                send(f"RESPONSE|{type}|{name}")

        else:
            print(f'[SERVER]:{msg}')        


thread = threading.Thread(target=listen,daemon = True)
thread.start()

try:
    while True:
        pass

except KeyboardInterrupt:
    print('Thankyou for visiting, Open for Feedback!..')
    print('Closing..')
    time.sleep(1)
    send(DISCONNECT_MSG)
    thread.join()
    client.close()
    sys.exit()