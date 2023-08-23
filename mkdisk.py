import os
import struct
import time
import random
from MBR import MBR
from PARTICION import Partition
def mkdisk(params):
    print("\n💽 creating disk...")
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
    #print(f"Current directory: {current_directory}")
    full_path= f'{current_directory}/discos_test{filename}'
    #path = os.path.join(current_directory, 'discos_test', filename)
    path = full_path
    #print(f"Full path: {path}")
    # If the directory does not exist, create it
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create or overwrite the binary file with specified size filled with zeroes
    with open(path, "wb") as file:
        file.write(b'\0' * total_size_bytes)

    print(f"**Disk created successfully at {path} with size {size}{unit}.")
    example = MBR(params)
    with open(path, "rb+") as file:
        file.seek(0)
        file.write(example.pack())
    #print(example)
    #get the full path of the file and print it
    #print(os.path.abspath(path))


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

import struct
def fdisk(params):
    print("\n📁 creating partition...")
    filename = params.get('path')
    current_directory = os.getcwd()
    full_path= f'{current_directory}/discos_test{filename}'
    #check if path exist and if so open the file, if not, return error
    if not os.path.exists(full_path):
        print(f"Error: The file {full_path} does not exist.")
        return
    #open the file and read the MBR
    nueva_particion = Partition(params)
    nueva_particion.status = 1
    particion_temporal = nueva_particion
    with open(full_path, "rb+") as file:
        for i in range(4):
            file.seek(struct.calcsize(MBR.FORMAT)+(i*Partition.SIZE))
            #unpack the partition
            data = file.read(Partition.SIZE)
            particion_temporal = Partition.unpack(data)
            if particion_temporal.status == 0:
                file.seek(struct.calcsize(MBR.FORMAT)+(i*Partition.SIZE))
                file.write(nueva_particion.pack())
                print(f"Partition {nueva_particion.name} created successfully.")
                return
        
        
    
    