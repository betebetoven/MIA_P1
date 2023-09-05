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
        superblock.s_free_inodes_count -= 1
        superblock.s_free_blocks_count -= 1 #for the superblock
        filename = path
        current_directory = os.getcwd()
        full_path= f'{current_directory}/discos_test{filename}'
        if not os.path.exists(full_path):
            print(f"Error: The file {full_path} does not exist.")
            return
        with open(full_path, "rb+") as file:
            file.seek(inicio)
            file.write(superblock.pack())
            bitmapinodos = ['0']*superblock.s_inodes_count
            bitmapbloques = ['0']*superblock.s_blocks_count
            bitmapbloques[0] = '1'
            bitmapinodos[0] = '1'
            for i in range(superblock.s_inodes_count):
                file.write(bitmapinodos[i].encode('utf-8'))
            for i in range(superblock.s_blocks_count):
                file.write(bitmapbloques[i].encode('utf-8'))
            #now write the inodes nex to the superblock we just wrote
            first_inode = Inode()
            first_inode.i_type = '0'
            first_inode.i_block[0] = 0
            first_bloque = FolderBlock()
            bitmapbloques[1] = '1'
            bitmapinodos[1] = '1'
            first_bloque.b_content[0].b_inodo = 1
            first_bloque.b_content[0].b_name = 'users.txt'
            inode_first_file = Inode()
            inode_first_file.i_type = '1'
            inode_first_file.i_block[0] = 1
            first_file_block = FileBlock()
            first_file_block.b_content = '1, G, root \n1, U, root, root, 123 \n0, G, usuarios \n'
            
            
            
            
            
            
            file.seek(superblock.s_inode_start)
            file.write(first_inode.pack())
            file.write(inode_first_file.pack())
            file.seek(superblock.s_block_start)
            file.write(first_bloque.pack())
            file.write(first_file_block.pack())
            

        


        print(f"Partition {id} was formatted successfully.")
