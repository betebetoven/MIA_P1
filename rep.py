from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content, Journal
import struct
import os
from MBR import MBR
from prettytable import PrettyTable
COLORS = {'Inode': 'lightblue', 'Superblock': '#E0E0E0', 'FolderBlock': '#FFCC00', 'FileBlock': 'green', 'PointerBlock': 'orange',  'Content': '#FFCC00'}
def imprimir(obj,index):
    object_type = type(obj).__name__
    if object_type == 'FileBlock':
        obj.b_content = obj.b_content.replace('\x00', '')
    if object_type == 'FolderBlock':
        for n in obj.b_content:
            n.b_name = n.b_name.replace('\x00', '')
    table = PrettyTable(['Attribute', 'Value'])
    attributes = vars(obj)
    lista = None
    for attr, value in attributes.items():
        if not isinstance(value, list):
            table.add_row([attr, value])
        else:
            lista = value
    return object_type, table, lista,index
current_id = 0

def get_next_id():
    global current_id
    current_id += 1
    return current_id
def prettytable_to_html_string(object_type, pt, lista,index, object):
    global current_id
    get_next_id()
    header_node = f'subgraph cluster_{object_type}{index} {"{"} label = "{object_type}{index}" style = filled fillcolor = "{COLORS[object_type]}"'
    nodo_tabla = f'\n{current_id} [label='
    html_string = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">\n'''
    html_string += "  <TR>\n"
    for field in pt._field_names:
        html_string += f"    <TD>{field}</TD>\n"
    html_string += "  </TR>\n"
    for row in pt._rows:
        html_string += "  <TR>\n"
        for cell in row:
            cell = str(cell).replace("\n", "<BR/>")
            html_string += f"    <TD>{cell}</TD>\n"
        html_string += "  </TR>\n"

    html_string += "</TABLE>> shape=box];\n"
    #if list is not none achieve this format bloques [label="{<content0> Content: users.txt | <content1> Content: empty | <content2> Content: empty | <content3> Content: empty}"];
    bloques = f'\nnode [shape=record];\nbloques{current_id} [label='
    if lista is not None:
        bloques += '"{'
        for i,n in enumerate(lista):
            bloques += f"<content{i}> {n.__str__()} | "
        bloques += '\n}"];'
    if lista is None:
        total = header_node + nodo_tabla + html_string + "}"
    else:
        total = header_node + nodo_tabla + html_string +  bloques + "}" 
    if object_type=='FolderBlock':
        total = header_node +  bloques + "}"

    return total,current_id

#0 inode, 1 folderblock, 2 fileblock, 3 pointerblock
codigo_para_graphviz = ''
def graph(file,inicio, index):
    global codigo_para_graphviz
    if inicio == -1:
        return None
    file.seek(inicio)
    if index == 0:
        object = Inode.unpack(file.read(Inode.SIZE))
    elif index == 1:
        object = FolderBlock.unpack(file.read(FolderBlock.SIZE))
    elif index == 2:
        object = FileBlock.unpack(file.read(FileBlock.SIZE))
    elif index == 3:
        object = PointerBlock.unpack(file.read(PointerBlock.SIZE))
    object_type, pt, lista,index = imprimir(object,inicio)
    total, id = prettytable_to_html_string(object_type, pt, lista,inicio, object)
    #print(f'///////////EL ID ES {id} DEL OBJETO {object_type} CON EL INDICE {inicio}*-*-*-*-*-*-*-*-*-*-*-*-*-*')
    codigo_para_graphviz += f'\n///////////EL ID ES {id} DEL OBJETO {object_type} CON EL INDICE {inicio}*-*-*-*-*-*-*-*-*-*-*-*-*-*'
    #print(total)
    codigo_para_graphviz += "\n"+total
    if object_type== 'Inode':
        for i,n in enumerate(lista):
            if object.i_type == '0':
                apuntado = graph(file,n,1)
                if apuntado is not None:
                    #print(f"bloques{id}:<content{i}> -> bloques{apuntado}")
                    codigo_para_graphviz += f"\nbloques{id}:<content{i}> -> bloques{apuntado}"
                
            else:
                apuntado =graph(file,n,2)
                if apuntado is not None:
                    #print(f"bloques{id}:<content{i}> -> {apuntado}")
                    codigo_para_graphviz += f"\nbloques{id}:<content{i}> -> {apuntado}"
    elif object_type== 'FolderBlock':
        for i,n in enumerate(lista):
            if n.b_inodo != -1:
                apuntado =graph(file,n.b_inodo,0)
                if apuntado is not None:
                    #print(f"bloques{id}:<content{i}> -> {apuntado}")
                    codigo_para_graphviz += f"\nbloques{id}:<content{i}> -> {apuntado}"
            
    
    return id


def rep(params, mounted_partitions): 
    global codigo_para_graphviz 
    #get params
    name = params.get('name', '')
    id = params.get('id', None)
    
    if id == None:
        print("Error: The id is required.")
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
        
        if name == 'tree':
            codigo_para_graphviz= ''

            primero = graph(file,superblock.s_inode_start,0)
            print(f"home -> {primero}")
            codigo_para_graphviz += f"\nhome -> {primero}"
            #print(codigo_para_graphviz)
            with open('graphvizcode.txt', 'w') as f:
                f.write(f'digraph G {{\n{codigo_para_graphviz}\n}}')