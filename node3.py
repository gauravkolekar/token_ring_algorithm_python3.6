# !/usr/bin/python
"""
    Name: Gaurav Vivek Kolekar
    Mav Id: 1001267145
"""

# this is node 1

# importing necessary libraries
import socket
import time
from contextlib import closing

# creating socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server socket timeout
server_socket.settimeout(30)

# host name is localhost
host = 'localhost'
port = 8888

# process id
p_id = 3

# waiting for token variable
delay = 5

# token flag
has_token = False

# binding the host and port number together
server_socket.bind((host, port))

# variable contains the data
data_token = None

# node 4 alive
node4_alive = 0

while True:

    print('waiting for token ...')

    # wait for token
    time.sleep(delay)

    try:
        data_token, sender_address = server_socket.recvfrom(1024)
        print(sender_address)
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            if sock.connect_ex(('127.0.0.1', 9999)) == 0:
                node4_alive = 0
            else:
                node4_alive = 1
        print('node 4 is alive', node4_alive)

    except socket.timeout:
        print('leader has failed !!!\n')
        print('Node 3: starting election !')
        election_msg = '3,'.encode()
        server_socket.sendto(election_msg, ('127.0.0.1', 8888))
        continue

    except socket.error:
        print('Node 4 is down')
        node4_alive = 1

    except Exception as e:
        print(e)
        print('no token received')
        data_token = None

    if data_token and sender_address[1] == 7777 and len(data_token) == 1 and data_token.decode() == '4':
        print('node 3 received: ', data_token)
        server_socket.sendto(data_token, ('127.0.0.1', 9999))

    elif data_token and sender_address[1] == 7777 and len(data_token) > 1 \
            and not data_token.decode().endswith('leader'):
        print('received token: ', data_token)
        data_token += '{},'.format(p_id).encode()
        print('modified data token', data_token)
        if node4_alive == 0:
            server_socket.sendto(data_token, ('127.0.0.1', 9999))
            print('sending to node 4')
        else:
            server_socket.sendto(data_token, ('127.0.0.1', 6666))
            print('sending to node 1')

    elif data_token and sender_address[1] == 7777 and len(data_token) > 1 \
            and data_token.decode().endswith('leader'):
        print('got leader message...')
        print(data_token)
        if node4_alive == 0:
            server_socket.sendto(data_token, ('127.0.0.1', 9999))
        else:
            server_socket.sendto(data_token, ('127.0.0.1', 6666))

    elif data_token and sender_address[1] == 7777 and len(data_token) == 1 and data_token.decode() == '3':
        print('node 3 received: ', data_token)
        if node4_alive == 0:
            server_socket.sendto(data_token, ('127.0.0.1', 9999))
        else:
            server_socket.sendto(data_token, ('127.0.0.1', 6666))

    else:
        print('reached ELSE block !!!!!')



server_socket.close()
# closing the server socket
