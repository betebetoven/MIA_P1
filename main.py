from ply.lex import lex
from ply.yacc import yacc

from mkdisk import mkdisk, rmdisk, fdisk
from comandos import comandos
from mount import mount, unmount
from mkfs import mkfs, login, makeuser
from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content


# --- Tokenizer

# All tokens must be named in advance.
tokens = ( 'MKDISK', 'SIZE', 'PATH', 'UNIT', 'FIT','ENCAJE',  
          'NAME',  
          'NOMBRE', 
          'NOMBREFEA',
          'UNIDAD', 
          'DIRECCION',
          'DIRECCIONFEA', 
          'NUMERO' , 
          'RMDISK',
          'FDISK',
          'TYPE',
          'TIPO',
          'DELETE',
          'DELETO',
          'ADD',
          'MOUNT',
          'ID',
          'IDENTIFICADOR',
          'UNMOUNT',
          'MKFS',
          'LOGIN',
          'USER',
          'PASSWORD',
          'CONTRA',
          'CONTRAFEA',
          'LOGOUT',
          'MKUSR', 
          'GRP')

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs

t_MKDISK = r'mkdisk'
t_MKFS = r'mkfs'
t_RMDISK = r'rmdisk'
t_FDISK = r'fdisk'
t_MOUNT = r'mount'
t_UNMOUNT = r'unmount'
t_LOGIN = r'login'
t_LOGOUT = r'logout'
t_MKUSR = r'mkusr'

t_USER = r'-user'
t_PASSWORD = r'-pass'
t_GRP = r'-grp'
t_NAME = r'-name'
t_ID = r'-id'
t_SIZE = r'-size='
t_PATH = r'-path='
t_UNIT = r'-unit='
t_FIT = r'-fit='
t_TYPE = r'-type='
t_DELETE = r'-delete='
t_ADD = r'-add='



# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMERO(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_DIRECCION(t):
    r'/[a-zA-Z0-9_\\/:.-]+.dsk'
    return t
def t_DIRECCIONFEA(t):
    r'"/[a-zA-Z0-9_\\/:. -]+.dsk"'
    t.value = t.value[1:-1]  # Strip the double quotes
    return t


def t_TIPO(t):
    r'(P|E|L)'
    return t
def t_DELETO(t):
    r'(FULL|full)'
    return t
    
def t_ENCAJE(t):
    r'(BF|FF|WF)'
    return t
def t_UNIDAD(t):
    r'(K|M|B)'
    return t
def t_NOMBRE(t):
    r'=[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value[1:]  # remove the '=' at the beginning
    return t
def t_NOMBREFEA(t):
    r'="[a-zA-Z_][a-zA-Z0-9_ ]*"'
    t.value = t.value[2:-1]  # remove the '=' at the beginning
    return t
def t_IDENTIFICADOR(t):
    r'=[0-9][0-9][0-9][a-zA-Z0-9_]+'
    t.value = t.value[1:]
    return t

def t_CONTRA(t):
    r'=[a-zA-Z0-9]+'
    t.value = t.value[1:]
    return t
def t_CONTRAFEA(t):
    r'="[a-zA-Z0-9]+"'
    t.value = t.value[2:-1]
    return t


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()
    
# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.
mounted_partitions = []
users=None
current_partition = None

def p_command_list(p):
    '''command_list : expression
                    | command_list expression'''
    if len(p) == 3:
        comandos = p[1]
        comandos.append(p[2])
        p[0] = comandos
    else:
        comandos = []
        comandos.append(p[1])
        p[0] = comandos




def p_expression(p):
    '''
    expression : mkdisk
                | rmdisk
                | fdisk
                | mount
                | unmount
                | mkfs
                | login
                | logout
                | mkusr
    '''

    p[0] = ('binop', p[1])

########################PARAMETROOOOOOOOOOOOOOOOOOOOOOOSSSSS
def p_name(p):
    '''
    nament : NAME NOMBRE
    '''
    p[0] = ('name', p[2])
def p_name2(p):
    '''
    nament : NAME NOMBREFEA
    '''
    p[0] = ('name', p[2])
def p_user(p):
    '''
    usernt : USER NOMBRE
    '''
    p[0] = ('user', p[2])
def p_user2(p):
    '''
    usernt : USER NOMBREFEA
    '''
    p[0] = ('user', p[2])
def p_grp(p):
    '''
    grpnt : GRP NOMBRE
    '''
    p[0] = ('grp', p[2])
def p_grp2(p):
    '''
    grpnt : GRP NOMBREFEA
    '''
    p[0] = ('grp', p[2])
def p_password(p):
    '''
    passnt : PASSWORD CONTRA
    '''
    p[0] = ('pass', p[2])
def p_password2(p):
    '''
    passnt : PASSWORD CONTRAFEA
    '''
    p[0] = ('pass', p[2])
def p_password3(p):
    '''
    passnt : PASSWORD NOMBRE
    '''
    p[0] = ('pass', p[2])
def p_password4(p):
    '''
    passnt : PASSWORD NOMBREFEA
    '''
    p[0] = ('pass', p[2])
def p_size(p):
    '''
    sizent : SIZE NUMERO
    '''
    p[0] = ('size', p[2])
def p_path(p):
    '''
    pathnt : PATH DIRECCION
    '''
    p[0] = ('path', p[2])    
def p_tipo(p):
    '''
    typent : TYPE TIPO
    '''
    p[0] = ('type', p[2])
def p_tipo2(p):
    '''
    typent : TYPE DELETO
    '''
    p[0] = ('type', p[2])    
def p_delete(p):
    '''
    deletent : DELETE DELETO
    '''
    p[0] = ('delete', p[2])
def p_add(p):
    '''
    addnt : ADD NUMERO
    '''
    p[0] = ('add', p[2])
def p_path2(p):
    '''
    pathnt : PATH DIRECCIONFEA
    '''
    p[0] = ('path', p[2])
def p_unit(p):
    '''
    unitnt : UNIT UNIDAD
    '''
    p[0] = ('unit', p[2])    
def p_fit(p):
    '''
    fitnt : FIT ENCAJE
    '''
    p[0] = ('fit', p[2])
def p_id(p):
    '''
    idnt : ID IDENTIFICADOR
    '''
    p[0] = ('id', p[2])
def p_param(p):
    '''
    param : sizent
          | pathnt
          | unitnt
          | fitnt
          | nament
          | typent
          | deletent
          | addnt
          | idnt
          | usernt
          | passnt
          | grpnt
            
    '''
    p[0] = p[1]    
def p_params(p):
    '''
    params : params param
           | param
    '''
    if len(p) == 3:
        p[0] = {**p[1], p[2][0]: p[2][1]}
    else:
        p[0] = {p[1][0]: p[1][1]}
#################################################FIN DE PARAMETROOOOOOOOOOOOSSSSSSSSSSSSSS
    
    
def p_mkdisk(p):
    '''
    mkdisk : MKDISK params
    '''
    #CREATE BINARY FILE
    mkdisk(p[2])
    p[0] = ('mkdisk', p[2])
    
def p_rmdisk(p):
    '''
    rmdisk : RMDISK params
    '''
    rmdisk(p[2])
    p[0] = ('rmdisk', p[2])

def p_fdisk(p):
    '''
    fdisk : FDISK params
    '''
    fdisk(p[2])
    p[0] = ('fdisk', p[2])   
def p_mount(p):
    '''
    mount : MOUNT params
    '''
    mount(p[2], mounted_partitions)
    print(mounted_partitions)
    p[0] = ('mount', p[2])

def p_unmount(p):
    '''
    unmount : UNMOUNT params
    '''
    unmount(p[2], mounted_partitions)
    p[0] = ('unmount', p[2])
def p_mkfs(p):
    '''
    mkfs : MKFS params
    '''
    mkfs(p[2], mounted_partitions, users)
    p[0] = ('mkfs', p[2])
def p_login(p):
    '''
    login : LOGIN params
    '''
    global users
    global current_partition
    users, current_partition = login(p[2], mounted_partitions)
    p[0] = ('login', p[2])
def p_logout(p):
    '''
    logout : LOGOUT
    '''
    global users
    exited_user = {}
    if users is not None:
        exited_user = users
        users = None
    else:
        print("No user is logged in")
    p[0] = ('logout', (exited_user))
def p_mkusr(p):
    '''
    mkusr : MKUSR params
    '''
    if users != None and users['username']=='root' :
        makeuser(p[2], mounted_partitions, current_partition)
    else:
        print("Error: You must be logged in as root to use this command")
    
    p[0] = ('mkusr', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse(comandos)

#read C:\Users\alber\OneDrive\Escritorio\cys\MIA\proyecto1\discos_test\home\mis discos\Disco4.dsk from the byte 0 an unpack it with MBR and print it
from MBR import MBR
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

with open(r'C:\Users\alber\OneDrive\Escritorio\cys\MIA\proyecto1\discos_test\home\mis discos\Disco4.dsk', "rb") as file:
    file.seek(0)
    data = file.read(MBR.SIZE)
    mbr = MBR.unpack(data[:MBR.SIZE])
    #print("este es el mbr____")
    #print(mbr)

    from prettytable import PrettyTable
    table = PrettyTable()
    table.field_names = ["Size", "Date", "Sig.", "Fit"]
    table.add_row([mbr.mbr_tamano, mbr.mbr_fecha_creacion, mbr.mbr_dsk_signature, mbr.fit])
    
    table2 = PrettyTable()
    table2.field_names = ["size", "name", "unit", "type", "status","fit","inicio"]
    for n in mbr.particiones:
        table2.add_row([n.actual_size, n.name, n.unit, n.type, n.status, n.fit, n.byte_inicio])
        
    
    print("👮🏼‍♂️_____________________MBR LEIDO__________________________________________________")
    print(table)
    print(table2)
    print("res")
    file.seek(mbr.particiones[0].byte_inicio)
    superblock = Superblock.unpack(file.read(Superblock.SIZE))
    codigo_para_graphviz= ''
    primero = graph(file,superblock.s_inode_start,0)
    print(f"home -> {primero}")
    codigo_para_graphviz += f"\nhome -> {primero}"
    with open('graphvizcode.txt', 'w') as f:
        f.write(f'digraph G {{\n{codigo_para_graphviz}\n}}')
    
    #file.seek(superblock.s_inode_start)
    #inodo = Inode.unpack(file.read(Inode.SIZE))
    #inodo2 = Inode.unpack(file.read(Inode.SIZE))
    #a,b,c,d = imprimir(inodo,0)
    #print( prettytable_to_html_string(a,b,c,d))
    #a,b,c,d = imprimir(inodo2,1)
    #print( prettytable_to_html_string(a,b,c,d))
    
    #print(inodo2)
    
    
def graph_sistema():
    code = "digraph G {"
    

    code += "}"

for n in ast:
    print(n[1])
print(users)
print(current_partition)
    
    
