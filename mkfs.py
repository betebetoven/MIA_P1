from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content
import os
import struct
import time
import random
def mkfs(params, mounted_partitions):
    tipo = params.get('type', 'full').lower()
    id = params.get('id', None)
    
    # Check if the id exists in mounted_partitions.
    partition = None
    for partition_dict in mounted_partitions:
        if id in partition_dict:
            partition = partition_dict[id]
            break

    if not partition:
        print(f"Error: The partition with id {id} does not exist.")
        return

    # Retrieve partition details.
    path = partition['path']
    inicio = partition['inicio']
    size = partition['size']

    # Step 3: Format based on tipo.
    if tipo == 'full':
        superblock = Superblock(inicio, size)
        filename = path
        current_directory = os.getcwd()
        full_path= f'{current_directory}/discos_test{filename}'
        if not os.path.exists(full_path):
            print(f"Error: The file {full_path} does not exist.")
            return
        with open(full_path, "rb+") as file:
            file.seek(inicio)
            file.write(superblock.pack())
            for i in range(superblock.s_inodes_count):
                file.write('I'.encode('utf-8'))
            for i in range(superblock.s_blocks_count):
                file.write('B'.encode('utf-8'))

        


        print(f"Partition {id} was formatted successfully.")
