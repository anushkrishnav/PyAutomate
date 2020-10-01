import os
import platform
from time import sleep
from moviepy.editor import *

os.system('clear')
operating_system = platform.system()

default_save_location = "Desktop/"
file_number = 1

continue_converting = 'y'
#main loop for converting files in case someone wants to do multiple files.
while continue_converting != 'n':
    
    default_file_name = "converted" + str(file_number) + ".mp3"

    #Check the user's operating system in order to save/check save location successfully.
    if operating_system == "Linux":
        mp3_path = os.path.join(os.path.join(
            os.path.expanduser('~')), default_save_location)
        mp4_path = mp3_path
    else:
        mp3_path = os.path.join(os.path.join(
            os.environ['USERPROFILE']), default_save_location)
        mp4_path = mp3_path

    change_mp4_path = input("The program will check your desktop for mp4 files, would you like to change the search location? [y/n]: ")
    if change_mp4_path == "y":
        mp4_path = input("Enter path to mp4 file you want to convert (include file and extension): ")
    else:
        mp4_name = input("Enter the name of the mp4 file (including extension): ")
        mp4_path += mp4_name

    change_save_location = input("Default save location is on the Desktop, would you like to save elsewhere? [y/n]: ")

    if change_save_location == "y":
        mp3_path = input("Enter custom save path: ")

    change_filename = input(f'Default audio file name is {default_file_name} would you like to change this? [y/n]: ')

    if change_filename == "y":
        mp3_filename = input("Enter new mp3 file name (including extension): ")
        mp3_path += mp3_filename
    else:
        mp3_path += default_file_name

    try:
        video = VideoFileClip(os.path.join(mp4_path))
    except OSError as e:
        print()
        print(f"** ERROR: the file at {mp4_path} could not be found! **")

    try:
        video.audio.write_audiofile(os.path.join(mp3_path))
    except NameError as e:
        print()
        print(f'** ERROR: Could not locate codec at path "{mp3_path}" **')
    except ValueError as e:
        print()
        print(f'** ERROR: Could not find the codec associated with the filename "{mp3_filename}" **')
    
    print()
    continue_converting = input("Would you like to convert antoher mp4 file? [y/n]: ")
    #increments the file number so you don't overwrite audio files if you choose to use the default file name and convert multiple files.
    file_number += 1
    os.system('clear')

print('Goodbye!')
sleep(1)
os.system('clear')
