# !/usr/bin/python
"""
    Name: Gaurav Vivek Kolekar
    Mav Id: 1001267145
"""

# this is node 4

# importing necessary libraries
import socket
import time

# creating socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# host name is localhost
host = 'localhost'
port = 9999

# process id
p_id = 4

# waiting for token variable
delay = 5

# token flag
has_token = False

# binding the host and port number together
server_socket.bind((host, port))

# variable contains the data
# data_token = '4'.encode()

# first_time
first_time = True

while True:

    print('waiting for token ...')

    # wait for token
    time.sleep(delay)
    if first_time:
        data_token = '4,'.encode()
        server_socket.sendto(data_token, ('127.0.0.1', 6666))
        first_time = False
        continue

    try:
        data_token, sender_address = server_socket.recvfrom(1024)
        print(sender_address)

    except:
        print('no token received')
        data_token = None

    if data_token and sender_address[1] == 8888 and len(data_token) == 1 and data_token.decode() == '4':
        print('node 4 received: ', data_token)
        server_socket.sendto(data_token, ('127.0.0.1', 6666))

    elif data_token and sender_address[1] == 8888 and len(data_token) == 1 and data_token.decode() == '3':
        continue

    elif data_token and sender_address[1] == 8888 and len(data_token) > 1 and \
            not data_token.decode().endswith('leader'):
        print('received token: ', data_token)
        if str(data_token).find(str(p_id)) > -1:
            print('found 4')
            data_token = data_token.decode()
            new_leader = max(data_token.split(','))
            print('new leader is: ', new_leader)
            new_leader_message = '4 says {} is new leader'.format(new_leader)
            new_leader_message = new_leader_message.encode()
            server_socket.sendto(new_leader_message, ('127.0.0.1', 6666))

    elif data_token and sender_address[1] == 8888 and len(data_token) > 1 and \
            data_token.decode().startswith('4') and data_token.decode().endswith('leader'):
        print('leader message reached everyone ...')
        server_socket.sendto(data_token.decode().split()[2].encode(), ('127.0.0.1', 6666))

    else:
        print('reached ELSE block !!!!')

server_socket.close()
# closing the server socket
