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
            
            bitmapinodos = ['0']*superblock.s_inodes_count
            bitmapbloques = ['0']*superblock.s_blocks_count
            
            #crea inodo 0
            i1 = Inode()
            i1.i_type = '0'
            i1.i_block[0] = superblock.s_block_start
            #crea bloque 0
            b1 = FolderBlock()
            b1.b_content[0].b_inodo = superblock.s_inode_start+Inode.SIZE
            b1.b_content[0].b_name = 'users.txt'
            bitmapbloques[0] = '1'
            bitmapinodos[0] = '1'
            
            
            #crea inodo 1
            i2 = Inode()
            i2.i_type = '1'
            i2.i_block[0] = superblock.s_block_start+block.SIZE
            #crea bloque 1
            b2 = FileBlock()
            b2.b_content = '1, G, root \n1, U, root, root, 123 \n0, G, usuarios \n'
            #b2.b_content='albertojosuuehernandezarmasdelalibertadalasnacionesdecritsojesusenlasalturasamen'
            bitmapbloques[1] = '1'
            bitmapinodos[1] = '1'
            
            
            
            file.seek(inicio)
            file.write(superblock.pack())
            for i in range(superblock.s_inodes_count):
                file.write(bitmapinodos[i].encode('utf-8'))
            for i in range(superblock.s_blocks_count):
                file.write(bitmapbloques[i].encode('utf-8'))
            file.seek(superblock.s_inode_start)
            file.write(i1.pack())
            file.write(i2.pack())
            file.seek(superblock.s_block_start)
            file.write(b1.pack())
            file.write(b2.pack())
            

        


        print(f"Partition {id} was formatted successfully.")
