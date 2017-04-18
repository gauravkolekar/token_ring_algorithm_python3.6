# !/usr/bin/python
"""
    Name: Gaurav Vivek Kolekar
    Mav Id: 1001267145
"""

# this is node 1

# importing necessary libraries
import socket
import time
import sys


# creating socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server socket timeout
server_socket.settimeout(21)

# host name is localhost
host = 'localhost'
port = 6666

# process id
p_id = 1

# time to wait for the token
delay = 5

# token flag
has_token = False

# binding the host and port number together
server_socket.bind((host, port))

# this variable will contain the data token
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
        print('Node 1: starting election !')
        election_msg = '1,'.encode()
        server_socket.sendto(election_msg, ('127.0.0.1', 7777))
        continue
    except Exception as e:
        print(str(e))
        print('reached general exception block')
        print('no token received')
        data_token = None

    if data_token and sender_address[1] == 9999 and len(data_token) == 1:
        print('node 1 received: ', data_token)
        server_socket.sendto(data_token, ('127.0.0.1', 7777))

    elif data_token and sender_address[1] == 9999 and len(data_token) > 1 and \
            not data_token.decode().endswith('leader'):
        print('received token: ', data_token)
        data_token += '{},'.format(p_id).encode()
        print('modified data token: ', data_token)
        server_socket.sendto(data_token, ('127.0.0.1', 7777))

    elif data_token and sender_address[1] == 9999 and len(data_token) > 1 and \
            data_token.decode().endswith('leader'):
        print('got leader message ...')
        print(data_token)
        server_socket.sendto(data_token, ('127.0.0.1', 7777))

    elif data_token and sender_address[1] == 8888 and len(data_token) == 1:
        print('node 1 received: ', data_token)
        server_socket.sendto(data_token, ('127.0.0.1', 7777))

    elif data_token and sender_address[1] == 8888 and len(data_token) > 1 and \
            not data_token.decode().endswith('leader'):
        print('received token: ', data_token)
        if str(data_token).find(str(p_id)) > -1:
            print('found 1')
            data_token = data_token.decode()
            new_leader = max(data_token.split(','))
            print('new leader is: ', new_leader)
            new_leader_message = '1 says {} is new leader'.format(new_leader)
            new_leader_message = new_leader_message.encode()
            server_socket.sendto(new_leader_message, ('127.0.0.1', 7777))

        else:
            print('received token: ', data_token)
            data_token += '{},'.format(p_id).encode()
            print('modified data token: ', data_token)
            server_socket.sendto(data_token, ('127.0.0.1', 7777))

    elif data_token and sender_address[1] == 8888 and len(data_token) > 1 and \
            data_token.decode().startswith('1') and data_token.decode().endswith('leader'):
        print('leader message reached everyone ...')
        server_socket.sendto(data_token.decode().split()[2].encode(), ('127.0.0.1', 7777))

    else:
        print('Reached General exception block')

server_socket.close()
# closing the server socket
