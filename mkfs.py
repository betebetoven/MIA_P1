from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content
import os
import struct
import time
import random
from mountingusers import load_users_from_content, parse_users, get_user_if_authenticated
def mkfs(params, mounted_partitions, users):
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
            b2.b_content = '1,G,root\n1,U,root,root,123\n'
            #b2.b_content+='2,G,usuarios\n2,U,usuarios,user1,usuario\n'
            #users.update(load_users_from_content(b2.b_content))
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
from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content
def login(params, mounted_partitions):
    print("ESTE ES EL LOGIN*************************************************")
    print(params)
#user, password need to come in params, if not, return error
    try:
        user = params['user']
        password = params['pass']
        id = params['id']
        
    except:
        print("Error: The user and password are required.")
        return None, None
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
    filename = path
    current_directory = os.getcwd()
    full_path= f'{current_directory}/discos_test{filename}'
    if not os.path.exists(full_path):
        print(f"Error: The file {full_path} does not exist.")
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock = Superblock.unpack(file.read(Superblock.SIZE))
        print("ESTE ES EL SUPERBLOCK EN EL LOGIN__________________")
        print(superblock)
        file.seek(superblock.s_inode_start)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        siguiente = inodo.i_block[0]
        file.seek(siguiente)
        folder = FolderBlock.unpack(file.read(FolderBlock.SIZE))
        siguiente = folder.b_content[0].b_inodo
        file.seek(siguiente)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        texto = ""
        for n in inodo.i_block:
            if n != -1:
                siguiente = n
                file.seek(siguiente)
                fileblock = FileBlock.unpack(file.read(FileBlock.SIZE))
                texto += fileblock.b_content.rstrip('\x00')
        print("ESTE ES EL TEXTO EN EL LOGIN__________________")
        
        #texto+='2,G,usuarios\n2,U,usuarios,user1,usuario\n'
        #usuarios = load_users_from_content(texto)
        usuarios = parse_users(texto)
        users= get_user_if_authenticated(usuarios, user, password)
        return users,id
        
def makeuser(params, mounted_partitions,id):
    print("ESTE ES EL MAKEUSER*************************************************")
    print(params)
    if id == None:
        print("Error: The id is required.")
        return
    try: 
        user = params['user']
        password = params['pass']
        group = params['grp']
    except:
        print("Error: The user, password and group are required.")
        return
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
    filename = path
    current_directory = os.getcwd()
    full_path= f'{current_directory}/discos_test{filename}'
    if not os.path.exists(full_path):
        print(f"Error: The file {full_path} does not exist.")
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock = Superblock.unpack(file.read(Superblock.SIZE))
        print("ESTE ES EL SUPERBLOCK EN EL MAKEUSER__________________")
        print(superblock)
        file.seek(superblock.s_inode_start)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        siguiente = inodo.i_block[0]
        file.seek(siguiente)
        folder = FolderBlock.unpack(file.read(FolderBlock.SIZE))
        siguiente = folder.b_content[0].b_inodo
        file.seek(siguiente)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        siguiente = inodo.i_block[0]
        file.seek(siguiente)
        fileblock = FileBlock.unpack(file.read(FileBlock.SIZE))
        texto = fileblock.b_content.rstrip('\x00')
        print("*********ESTE ES EL TEXTO EN EL MAKEUSER__________________")
        print(texto)
        
        
        
    