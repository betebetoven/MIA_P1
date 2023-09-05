from ply.lex import lex
from ply.yacc import yacc

from mkdisk import mkdisk, rmdisk, fdisk
from comandos import comandos
from mount import mount, unmount
from mkfs import mkfs
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
          'MKFS',)

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs

t_MKDISK = r'mkdisk'
t_MKFS = r'mkfs'
t_RMDISK = r'rmdisk'
t_FDISK = r'fdisk'
t_MOUNT = r'mount'
t_UNMOUNT = r'unmount'


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
    mkfs(p[2], mounted_partitions)
    p[0] = ('mkfs', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse(comandos)

#read C:\Users\alber\OneDrive\Escritorio\cys\MIA\proyecto1\discos_test\home\mis discos\Disco4.dsk from the byte 0 an unpack it with MBR and print it
from MBR import MBR
def imprimir(obj):
    # Create a table with two columns: "Attribute" and "Value"
    object_type = type(obj).__name__

    print(f"Object Type: {object_type}")
    table = PrettyTable(['Attribute', 'Value'])

    # Use the built-in vars() function to get object's attributes
    attributes = vars(obj)

    # Add each attribute and its value as a row in the table
    for attr, value in attributes.items():
        table.add_row([attr, value])

    # Print the table
    print(table)
    return table
def prettytable_to_html_string(pt):
    html_string = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">\n'''
    # Header
    html_string += "  <TR>\n"
    for field in pt._field_names:
        html_string += f"    <TD>{field}</TD>\n"
    html_string += "  </TR>\n"

    # Rows
    for row in pt._rows:
        html_string += "  <TR>\n"
        for cell in row:
            html_string += f"    <TD>{cell}</TD>\n"
        html_string += "  </TR>\n"

    html_string += "</TABLE>>"

    return html_string
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
    imprimir(superblock)
    file.seek(superblock.s_inode_start)
    inodo = Inode.unpack(file.read(Inode.SIZE))
    imprimir(inodo)
    file.seek(superblock.s_block_start)
    folderblock = FolderBlock.unpack(file.read(FolderBlock.SIZE))
    print("__folderblock__")
    for i,n in enumerate(folderblock.b_content):
        print(i)
        imprimir(n)
    print("_______________")
    file.seek(superblock.s_inode_start+Inode.SIZE)
    inodo = Inode.unpack(file.read(Inode.SIZE))
    imprimir(inodo)
    file.seek(superblock.s_block_start+FolderBlock.SIZE)
    fileblock = FileBlock.unpack(file.read(FileBlock.SIZE))
    print(prettytable_to_html_string(imprimir(fileblock)))

for n in ast:
    print(n[1])
    
    
