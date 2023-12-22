"""
Author: Oleg Shkolnik יא9.
Description: Server that makes one of available commands (DIR/DELETE/COPY/EXECUTE/TAKE_SCREEN/SEND_SCREEN/EXIT:) and sends result to client
Date: 10/12/23
"""

import socket
from functions import *
from protocol import *

MAX_PACKET = 2048
QUEUE_LEN = 1
IP = "127.0.0.1"
PORT = 5746

ERR = 'Invalid command. Available commands are: DIR, DELETE, COPY, EXECUTE, TAKE_SCREEN, SEND_SCREEN, EXIT:'
COMMANDS = ['DIR', 'DELETE', 'COPY', 'EXECUTE', 'TAKE_SCREEN', 'SEND_SCREEN', 'EXIT']


def make_command_info(request: str, path: str):
    """
    runs the desired function in which we need more information(path or file)
    :param request: command
    :param path: path or file
    :return: result of the running function
    """
    if request == COMMANDS[0]:
        response = direct(path)

    elif request == COMMANDS[1]:
        response = delete(path)

    elif request == COMMANDS[2]:
        response = copy(path)

    elif request == COMMANDS[3]:
        response = execute(path)

    else:
        response = False

    return response


def make_command_without_info(request: str):
    """
    runs the desired function in which we need tp know only command
    :param request: command
    :return: result of the running function
    """
    if request == COMMANDS[4]:
        response = take_screen()

    else:
        response = False

    return response


def main():
    """
    Setting ip and port
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        """
        Set upping server
        """
        my_socket.bind((IP, PORT))
        my_socket.listen(QUEUE_LEN)

        while True:
            """
            Server is always ready to connect new client
            """
            client_socket, client_address = my_socket.accept()

            try:

                while True:
                    """
                    Gets request and divides it on command and path (if it exists)
                    Making command
                    Sending result of command execution
                    """

                    request = recv(client_socket)
                    if request == None:
                        break
                    t = True
                    path = ''

                    for i in range(len(request) - 1):
                        if request[i] == ' ':
                            t = False

                    if not t:
                        temp = request.split(' ')
                        cmd = temp[0]
                        path = temp[1]

                    else:
                        cmd = request

                    print('server received ' + request)

                    if cmd == 'EXIT':
                        break
                    elif cmd in COMMANDS[:4]:
                        response = make_command_info(cmd, path)
                        send(client_socket, response)

                    elif cmd == COMMANDS[5]:
                        data = send_file(client_socket)
                        print(data)

                    elif cmd in COMMANDS[4:]:
                        response = make_command_without_info(cmd)
                        send(client_socket, response)

                    else:
                        response = 'Cant do this command now'
                        send(client_socket, response)

            except socket.error as err:
                """
                Send the name of error in error situation
                """
                print('received socket error on client socket' + str(err))

            finally:
                """
                Close the socket anyway
                """
                client_socket.close()

    except socket.error as err:
        """
        Send the name of error in error situation
        """
        print('received socket error on server socket' + str(err))

    finally:
        """
        Close the socket anyway
        """
        my_socket.close()


if __name__ == '__main__':
    """
    checking function situations and launching the main
    """
    assert make_command_info('DIR', r'C:\Users\Олег\PycharmProjects\Improved_Commands')
    assert make_command_info('DELETE', r'A.txt')
    assert make_command_info('COPY', r'B.txt;A.txt')
    assert make_command_info('EXECUTE', r'note.exe')
    assert make_command_without_info('TAKE_SCREEN')
    assert not make_command_info('Oleg', r'A.txt')
    assert not make_command_without_info('Oleg')

    main()
