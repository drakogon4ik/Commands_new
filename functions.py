"""
Author: Oleg Shkolnik יא9.
Description: functions for server and client
Date: 10/12/23
"""


import glob
import os
import subprocess
import pyautogui
import shutil
from protocol import *
from base64 import *


MAX_PACKET = 2048


def direct(place):
    """
    searches all files in the specified path
    :param place: user's path
    :return: all files in specified path
    """

    try:
        files_list = glob.glob(r'' + place + r'\*.*')
        return '\n'.join(files_list)

    except os.error as err:
        return f'received error {str(err)}'


def delete(place):
    """
    deletes specified file
    :param place: file user want to delete
    :return: message about result of function's work
    """
    try:
        os.remove(r'' + place)
        return f'file was deleted successfully'
    except os.error as err:
        return f"file wasn't deleted due to error {str(err)}"


def copy(files):
    """
    copies specified file in another specified file
    :param files: two files separated by ';'
    :return: message about result of function's work
    """
    try:
        places = files.split(';')

        shutil.copy(r'' + places[0], r'' + places[1])
        return f'file was copied successfully'
    except os.error as err:
        return f"file wasn't copied due to error {str(err)}"


def execute(program):
    """
    executes specified application
    :param program: application
    :return: message about result of function's work
    """
    try:
        subprocess.call(r'' + program)
        return f"file was opened successfully"
    except os.error as err:
        return f"file wasn't opened due to error {str(err)}"


def take_screen():
    """
    takes screenshot and saves it
    :return: message about result of function's work
    """
    try:
        image = pyautogui.screenshot()
        image.save('screen.jpg')
        return 'success'
    except os.error as err:
        return f"screenshot wasn't taken due to error {str(err)}"


def send_file(socket):
    """
    sends picture to the client using base64 module to be able to receive and write bytes
    :param socket: socket, to which we send
    :return: message about result of function's work
    """
    try:
        with open('screen.jpg', mode='rb') as screen:
            response = b64encode(screen.read())
            len_data = struct.pack(form, len(response))
            socket.sendall(len_data + response)
        return 'picture was sent successfully'
    except os.error as err:
        return f"screenshot wasn't taken due to error {str(err)}"


def receive_file(socket):
    """
    fills the file with the received data(data was encoded with module base64, so it is bytes)
    :param socket: socket, from which we receive
    :return: message about result of function's work
    """
    try:
        with open('screen1.jpg', mode='wb') as screen:
            response = b64decode(recv(socket))
            screen.write(response)
        return 'success'
    except os.error as err:
        return f"screenshot wasn't taken due to error {str(err)}"


if __name__ == '__main__':
    """
    checking function situations and launching the main
    """
    assert direct(r'C:\Users\Олег\PycharmProjects\Improved_Commands')
    assert delete(r'A.txt')
    assert copy(r'B.txt;A.txt')
    assert execute(r'notepad.exe')
    assert take_screen()
