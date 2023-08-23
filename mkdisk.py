import os
import struct
import time
import random
from MBR import MBR
def mkdisk(params):
    # Extract parameters with defaults if not provided
    size = params.get('size')
    filename = params.get('path')
    unit = params.get('unit', 'M')
    fit = params.get('fit', 'FF')

    # Check mandatory parameters
    if not size or not filename:
        print("Both -size and -path parameters are mandatory!")
        return

    # Calculate total size in bytes
    if unit == 'K':
        total_size_bytes = size * 1024
    elif unit == 'M':
        total_size_bytes = size * 1024 * 1024
    else:
        print(f"Invalid unit: {unit}")
        return

    # Check fit value
    if fit not in ['BF', 'FF', 'WF']:
        print(f"Invalid fit value: {fit}")
        return

    current_directory = os.getcwd()
    print(f"Current directory: {current_directory}")
    full_path= f'{current_directory}/discos_test{filename}'
    #path = os.path.join(current_directory, 'discos_test', filename)
    path = full_path
    print(f"Full path: {path}")
    # If the directory does not exist, create it
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create or overwrite the binary file with specified size filled with zeroes
    with open(path, "wb") as file:
        file.write(b'\0' * total_size_bytes)

    print(f"Disk created successfully at {path} with size {size}{unit}.")
    example = MBR(params)
    with open(path, "rb+") as file:
        file.seek(0)
        file.write(example.pack())
    print(example)
    #get the full path of the file and print it
    print(os.path.abspath(path))


def rmdisk(params):
    filename = params.get('path')

    # Check mandatory parameter
    if not filename:
        print("-path parameter is mandatory!")
        return

    # Get the full path to the file
    current_directory = os.getcwd()
    full_path = f'{current_directory}/discos_test{filename}'

    # If the file does not exist, show an error
    if not os.path.exists(full_path):
        print(f"Error: The file {full_path} does not exist.")
        return

    # Prompt user for confirmation before deletion
    response = input(f"Are you sure you want to delete {full_path}? (yes/no): ").strip().lower()

    if response == 'yes':
        os.remove(full_path)
        print(f"Disk {full_path} deleted successfully.")
    elif response == 'no':
        print("Disk deletion aborted.")
    else:
        print("Invalid response. Disk not deleted.")
