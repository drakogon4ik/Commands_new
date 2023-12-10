"""
Author: Oleg Shkolnik יא9.
Description: protocol with send and receive functions
Date: 10/12/23
"""


import struct


form = '>I'


def send(socket, data):
    """
    Data sending function
    :param socket: socket, to which we send
    :param data: data for sending
    :return: - (We send a struct of 4 bytes in size, storing the length of the message. The data contains 4 bytes storing the length of the message, plus the message itself.)
    """
    data = data.encode()

    len_data = struct.pack(form, len(data))

    socket.sendall(len_data + data)


def recv_packets(socket, n):
    """
    additional function to get packed data
    Until we get a piece of data of the required length
    We read a section of no more length than we are short of the required length
    :param socket: socket, from which we receive
    :param n: number of bytes of the encrypted message
    :return: packed data
    """
    piece = b''
    while len(piece) < n:

        packet = socket.recv(n - len(piece))

        if not packet:
            return None
        piece += packet
    return piece


def recv(socket):
    """
    Function for reading received data
    :param socket: socket, from which we receive
    :return: decoded data
    """
    length_data = recv_packets(socket, 4)

    if not length_data:
        return None

    data_len = struct.unpack(form, length_data)[0]

    return recv_packets(socket, data_len).decode()
