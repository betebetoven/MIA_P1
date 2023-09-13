from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content
import os
import struct
import time
import random
from mountingusers import load_users_from_content, parse_users, get_user_if_authenticated, get_id_by_group, extract_active_groups,get_group_id
from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content
import struct
from prettytable import PrettyTable
import re
from mkfile import busca
from mkfs import parse_users
def read_file_inode(file, lista):
    texto = ''
    for n in lista:
        if n == -1:
            continue
        file.seek(n)
        fileblock = FileBlock.unpack(file.read(FileBlock.SIZE))
        texto += fileblock.b_content.rstrip('\x00')
    return texto
        
def chown(params, mounted_partitions,id, usuario_actual):  
    print(f'CHOWN {params}')
    if id == None:
        print("Error: The id is required.")
        return
    try: 
        insidepath = params['path']
        user = params['user']
    except:
        print("Error:Path must be specified.")
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
        
        lista_direcciones = insidepath.split('/')[1:]
        PI = superblock.s_inode_start
        for i,n in enumerate(lista_direcciones):
            esta,v = busca(file,PI,0,n)
            if esta:
                PI = v
            else:
                print(f'archivo {insidepath} no existe')
                return
        file.seek(PI)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        print(inodo.i_uid)
        print(usuario_actual['id'])
        if str(inodo.i_uid) != str(usuario_actual['id']):
            print(f'No tiene permisos para cambiar el propietario del archivo {insidepath}')
            return
        
        _,PI_users = busca(file,superblock.s_inode_start,0,'users.txt')
        file.seek(PI_users)
        inodo_archivo = Inode.unpack(file.read(Inode.SIZE))
        texto_usuarios = read_file_inode(file, inodo_archivo.i_block)
        #print(texto_usuarios)
        grupos = parse_users(texto_usuarios)
        usuario_obtenido = None
        for n in grupos:
            if user in n:
                usuario_obtenido = n
                break
        print(usuario_obtenido)
        input()
        if usuario_obtenido:
            inodo.i_uid = int(usuario_obtenido[user]['id'])
            inodo.I_gid = int(usuario_obtenido[user]['id'])
            file.seek(PI)
            file.write(inodo.pack())
            print(f'El propietario del archivo {insidepath} ha sido cambiado a {user}')
            