import socket
import select
import errno
import sys
import time
from datetime import datetime

TIME_LENGTH = 5
HEADER_LENGTH = 30
ENCODING = 'utf-8'

HOSTNAME = socket.gethostname()
PORT = 1024
MY_FORMAT = u'%H:%M'

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOSTNAME, PORT))
client_socket.setblocking(False)

time = datetime.now().strftime(MY_FORMAT)
username = my_username.encode(ENCODING)
username_header = f"{len(username):<{HEADER_LENGTH}}".encode(ENCODING)
time = f"{time:<{TIME_LENGTH}}".encode(ENCODING)
client_socket.send(time + username_header + username)

while True:
    
    time = datetime.now().strftime(MY_FORMAT)

    message = input(f'[{f"{time}"}] {my_username} > ')

    if message:
        message = message.encode(ENCODING)
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode(ENCODING)
        time = f"{time:<{TIME_LENGTH}}".encode(ENCODING)
        client_socket.send(time + message_header + message)

    try:
        while True:

            time = client_socket.recv(TIME_LENGTH).decode(ENCODING).strip()
            # print('time: {}'.format(time))
            
            username_header = client_socket.recv(HEADER_LENGTH)
            # print('username_header: {}'.format(username_header))

            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode(ENCODING).strip())
            # print('username_length: {}'.format(username_length))

            username = client_socket.recv(username_length).decode(ENCODING)
            # print('username: {}'.format(username))

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode(ENCODING).strip())
            message = client_socket.recv(message_length).decode(ENCODING)

            print(f'[{time}] {username} > {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print('Reading error: {}'.format(str(e)))
        sys.exit()