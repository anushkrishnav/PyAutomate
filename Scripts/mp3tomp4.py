import os
import platform
from time import sleep
from moviepy.editor import *


def mp4_conversion(mp4_path, mp3_path):
    try:
        video = VideoFileClip(os.path.join(mp4_path))
    except OSError as e:
        print()
        print(f"** ERROR: the file at {mp4_path} could not be found! **")
        print()

    try:
        video.audio.write_audiofile(os.path.join(mp3_path))
    except NameError as e:
        print()
        print(f'** ERROR: Could not locate codec at path "{mp3_path}" **')
        print()
    except ValueError as e:
        print()
        print(f'** ERROR: Could not find the codec associated with the path"{mp3_path}" **')
        print('** Make sure to add the extension ".mp3" to the file name. **')
        print()


os.system('clear')
operating_system = platform.system()

default_save_location = "Desktop/"
file_number = 1


continue_converting = 'y'
#main loop for converting files in case someone wants to do multiple files.
while continue_converting != 'n':
    
    default_file_name = "converted" + str(file_number) + ".mp3"


    multiple_files = input("Are you converting multiple files or a single mp4 file? [s/m]: ")

    if multiple_files == 's':
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
        
        mp4_conversion(mp4_path, mp3_path)

    else:
        mp4_folder_path = input("Enter path to folder containing mp4 files: ")
        mp3_folder_path = input("Enter destination path for mp3 files: ")

        mp4_files = []
        for (dirpath, dirnames, filenames) in os.walk(mp4_folder_path):
            for file in filenames:
                if file[-3:] == "mp4":
                    mp4_files.append(file)
        
        name_files = input(f'The files are named "{default_file_name}" and increment by one by default. Would you like to name them uniquely? [y/n]: ')
        if name_files == "n":
            for file in mp4_files:
                default_file_name = "converted" + str(file_number) + ".mp3"
                mp4_conversion(mp4_folder_path + file, mp3_folder_path + default_file_name)
                file_number += 1
        else:
            for file in mp4_files:
                name = input("Enter name for this file (include extension): ")
                mp4_conversion(mp4_folder_path + file, mp3_folder_path + name)

    print()
    continue_converting = input("Would you like to convert more mp4 files? [y/n]: ")
    #increments the file number so you don't overwrite audio files if you choose to use the default file name and convert multiple files.
    file_number += 1
    os.system('clear')

print('Goodbye!')
sleep(1)
os.system('clear')
