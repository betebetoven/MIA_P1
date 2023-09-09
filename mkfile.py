from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content
import os
import struct
import time
import random
from mountingusers import load_users_from_content, parse_users, get_user_if_authenticated, get_id_by_group, extract_active_groups,get_group_id
from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content
import struct
def busca(file,byte,tipo,x):
    if tipo == 0:
        file.seek(byte)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        if inodo.i_type == 1:
            return False, None
        esta = False
        v = None
        for n in inodo.i_block:
            if n == -1:
                continue
            esta,v = busca(file,n,1,x)
            if esta:
                break
        return esta,v
    elif tipo == 1:
        file.seek(byte)
        folder = FolderBlock.unpack(file.read(FolderBlock.SIZE))
        esta = False
        v = None
        for n in folder.b_content:
            if n.b_inodo == -1:
                continue
            if n.b_name == x:
                esta = True
                v = n.b_inodo
                break
        return esta,v
    
def mkfile(params, mounted_partitions,id):
    print("ESTE ES EL MAKEUSER*************************************************")
    #print(params)
    if id == None:
        print("Error: The id is required.")
        return
    try: 
        insidepath = params['path']
        r = params.get('r', '/')
        archivosize = params.get('size', 0)
        archivocont = params.get('cont', '')
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
        file.seek(superblock.s_inode_start)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        
