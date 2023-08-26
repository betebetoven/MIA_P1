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
    
    
    #read all 4 partitions
    partitions = []
    with open(full_path, "rb+") as file:
        file.seek(0)
        data = file.read(MBR.SIZE)
        disk_size = MBR.unpack(data[:MBR.SIZE]).mbr_tamano
        print("disk size ",disk_size)
        space = disk_size - MBR.SIZE
        
        
        
        for i in range(4):
            file.seek(struct.calcsize(MBR.FORMAT)+(i*Partition.SIZE))
            #unpack the partition
            data = file.read(Partition.SIZE)
            particion_temporal = Partition.unpack(data)
            partitions.append(particion_temporal)
        realizar = True
        if all(item.status == 1 for item in partitions):
            realizar = False
            print("No se puede crear la particion, ya que todas las particiones estan ocupadas")
        count_E = sum(1 for item in partitions if item.type == 'E')
        if count_E == 1 and nueva_particion.type == 'E':
            realizar = False
            print("No se puede crear la particion, ya que ya existe una particion extendida")
        
        partitions2 = partitions
        byteinicio = MBR.SIZE
        if nueva_particion.fit == 'FF' and realizar:
            for i, item in enumerate(partitions):   
                if (item.status == 0 and item.name == "empty") or (item.status ==0 and space >= nueva_particion.actual_size):   
                    if i == 0:
                        byteinicio = MBR.SIZE
                    else :
                        byteinicio = partitions[i-1].byte_inicio+partitions[i-1].actual_size
                    probable = byteinicio+nueva_particion.actual_size
                    permiso = True
                    for j, item2 in enumerate(partitions2[(i+1):]):
                        if probable > item2.byte_inicio and item2.byte_inicio != 0:
                            permiso = False
                        
                    if permiso == True:        
                        nueva_particion.byte_inicio = byteinicio
                        partitions[i] = nueva_particion
                        item = nueva_particion
                        print(f"Partition {partitions[i]} created successfully.")
                        break 
            packed_objetos = b''.join([obj.pack() for obj in partitions])
            file.seek(struct.calcsize(MBR.FORMAT))
            file.write(packed_objetos)
            return 
        elif nueva_particion.fit == 'BF' and realizar:
            sale = space+1
            indice = -1
            for i,n in enumerate(partitions):
                print("i ",i)
                if (n.status == 0 and n.name == "empty") and (i==0 or partitions[i-1].status == 1):
                    if i == 0:
                        anterior = MBR.SIZE
                    else :
                        anterior = partitions[i-1].byte_inicio+partitions[i-1].actual_size
                        
                    siguiente = -1    
                    
                    
                    if i == 3 and n.status == 0:
                        siguiente = disk_size
                    for j, n2 in enumerate(partitions2[(i+1):]):
                        print("j ",j)
                        if n2.status == 1:
                            siguiente = n2.byte_inicio
                            break
                        elif j ==len(partitions2[(i+1):])-1 and n2.status == 0:
                            siguiente = disk_size
                            
                    print("siguiente ",siguiente)
                    print("anterior ",anterior)
                    print("actual size ",nueva_particion.actual_size)
                    print("sale ",sale)
                    espacio = siguiente-anterior
                    print("espacio ",espacio)
                    print(nueva_particion.actual_size <= espacio and espacio < sale)
                    
                    
                    if nueva_particion.actual_size <= espacio and espacio < sale:
                        sale = espacio
                        print("--------sale ",sale)
                        indice = i
                        print("---------indice ",indice)
                        byteinicio = anterior
                        print("---------byteinicio ",byteinicio)
                
            nueva_particion.byte_inicio = byteinicio
            partitions[indice] = nueva_particion
            #print len size of partitions
            print("partitions size ",len(partitions))
            
            print(f"se escribio la particion en el indice {indice}")
            packed_objetos = b''.join([obj.pack() for obj in partitions])
            file.seek(struct.calcsize(MBR.FORMAT))
            file.write(packed_objetos)
            return
            
            
              
    #le mandamos el pack     
    
    
     
            
    
    
    