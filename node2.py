# !/usr/bin/python
"""
    Name: Gaurav Vivek Kolekar
    Mav Id: 1001267145
"""

# this is node 2

# importing necessary libraries
import socket
import time

# creating socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server socket timeout
#server_socket.settimeout(15)
server_socket.settimeout(21)

# host name is localhost
host = 'localhost'
port = 7777

# process id
p_id = 2

# waiting for token variable
delay = 5

# token flag
has_token = False

# binding the host and port number together
server_socket.bind((host, port))

# variable contains the data
data_token = None

while True:

    print('waiting for token ...')

    # wait for token
    time.sleep(delay)

    try:
        data_token, sender_address = server_socket.recvfrom(1024)
        print(sender_address)

    except socket.timeout:
        print('leader has failed !!!\n')
        print('Node 2: starting election !')
        election_msg = '2,'.encode()
        server_socket.sendto(election_msg, ('127.0.0.1', 8888))
        continue

    except:
        print('no token received')
        data_token = None

    if data_token and sender_address[1] == 6666 and len(data_token) == 1:
        print('node 2 received: ', data_token)
        server_socket.sendto(data_token, ('127.0.0.1', 8888))

    elif data_token and sender_address[1] == 6666 and len(data_token) > 1 and \
            not data_token.decode().endswith('leader'):
        if data_token.decode().find(str(p_id)) > -1:
            print('found 2')
            data_token = data_token.decode()
            new_leader = max(data_token.split(','))
            print('new leader is: ', new_leader)
            new_leader_message = '2 says {} is new leader'.format(new_leader)
            new_leader_message = new_leader_message.encode()
            server_socket.sendto(new_leader_message, ('127.0.0.1', 8888))

        else:
            print('received token: ', data_token)
            data_token += '{},'.format(p_id).encode()
            print('modified data token: ', data_token)
            server_socket.sendto(data_token, ('127.0.0.1', 8888))

    elif data_token and sender_address[1] == 6666 and len(data_token) > 1 and \
            data_token.decode().startswith('2') and data_token.decode().endswith('leader'):
        print('leader message reached everyone ...')
        server_socket.sendto(data_token.decode().split()[2].encode(), ('127.0.0.1', 8888))

    elif data_token and sender_address[1] == 6666 and len(data_token) > 1 and \
            data_token.decode().endswith('leader'):
        print('got leader message ...')
        print(data_token)
        server_socket.sendto(data_token, ('127.0.0.1', 8888))
        print('sent to node 3')

    else:
        print('reached ELSE block ...')

server_socket.close()
# closing the server socket
