"""
Author: Oleg Shkolnik יא9.
Description: Client that receives input commands from cmd, sends them to the server, receives result and prints it
Date: 10/12/23
"""

import socket
from functions import receive_file
from protocol import *

IP = "127.0.0.1"
PORT = 5746
MAX_PACKET = 2048

PROMPT = 'Please enter a command(DIR, DELETE, COPY, EXECUTE, TAKE_SCREEN, SEND_SCREEN, EXIT): '
ERR = '\n Invalid command. Available commands are: DIR, DELETE, COPY, EXECUTE, TAKE_SCREEN, SEND_SCREEN, EXIT \n'
COMMANDS = ['DIR', 'DELETE', 'COPY', 'EXECUTE', 'TAKE_SCREEN', 'SEND_SCREEN', 'EXIT']
ASK_DIR = 'Please enter the path to the place where you wanna check files: '
ASK_DELETE = 'Please enter the path to the file that you wanna delete: '
ASK_COPY = 'Please enter the path to the file u wanna copy and the path to the new file through ";": '
ASK_EXECUTE = 'Please enter the name of the file that you wanna execute: '


def validate_command_info(cmd: str):
    """
    Validates that the user input is in 4 first commands that need additional information (path or file)
    :param cmd: the user command
    :return: true if the command is valid
    """
    return cmd in COMMANDS[:4]


def validate_command_without_info(cmd: str):
    """
    Validates that the user input is in 3 last commands that don't need additional information
    :param cmd: the user command
    :return: true if the command is valid
    """
    return cmd in COMMANDS[4:]


def asking_for_info(cmd: str):
    """
    asks for additional information (path or file) depending on the required function
    :param cmd: command
    :return: additional information (path or file)
    """
    place = ''

    if cmd == COMMANDS[0]:
        place = input(ASK_DIR)

    elif cmd == COMMANDS[1]:
        place = input(ASK_DELETE)

    elif cmd == COMMANDS[2]:
        place = input(ASK_COPY)

    elif cmd == COMMANDS[3]:
        place = input(ASK_EXECUTE)

    return place


def main():
    """
    Main function that connect client to server
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        """
        Connecting
        """
        my_socket.connect((IP, PORT))
        request = input(PROMPT)

        while request != COMMANDS[6]:
            """
            Loop until getting EXIT
            Validates if request in commands and sends it (with additional information (path or file) it it needs)
            receives result and prints it
            """

            if validate_command_info(request):

                path = asking_for_info(request)
                request = request + ' ' + path
                send(my_socket, request)
                data = recv(my_socket)
                print(data)

            elif request == COMMANDS[5]:
                send(my_socket, request)
                data = receive_file(my_socket)
                print(data)

            elif validate_command_without_info(request):
                send(my_socket, request)
                data = recv(my_socket)
                print(data)

            else:
                print(ERR)

            request = input(PROMPT)

        """
        After the loop send message and go to finally closing socket
        """
        print('bye bye')

    except socket.error as err:
        """
        Send the name of error in error situation
        """
        print('received socket error ' + str(err))

    finally:
        """
        Close the socket anyway
        """
        my_socket.close()


if __name__ == '__main__':
    """
    checking function situations and launching the main
    """
    assert validate_command_info('DIR')
    assert validate_command_info('DELETE')
    assert validate_command_info('COPY')
    assert validate_command_info('EXECUTE')
    assert validate_command_without_info('TAKE_SCREEN')
    assert validate_command_without_info('SEND_SCREEN')
    assert validate_command_without_info('EXIT')
    assert not validate_command_info('Oleg')
    assert not validate_command_without_info('Oleg')
    assert not asking_for_info('Oleg')
    main()
