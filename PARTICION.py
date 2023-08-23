import os
import struct
import time
import random
class Partition:
    # Using a format to capture size(int), path(string of 100 chars), name(string of 16 chars), unit(char)
    FORMAT = 'i 16s c'
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, params):
        # Extracting size from params
        self.actual_size = params.get('size')
        if self.actual_size < 0:
            raise ValueError("Size must be a positive integer greater than 0")

        # Extracting path from params

        # Extracting name from params
        self.name = params.get('name')
        if not self.name:
            raise ValueError("Partition name cannot be empty")

        # Extracting unit from params, default is 'K'
        self.unit = params.get('unit', 'K').upper()
        if self.unit not in ['B', 'K', 'M']:
            raise ValueError(f"Invalid unit: {self.unit}")

        # Calculate actual size based on unit
        if self.unit == 'B':
            self.actual_size = self.actual_size
        elif self.unit == 'K':
            self.actual_size = self.actual_size * 1024
        elif self.unit == 'M':
            self.actual_size = self.actual_size * 1024 * 1024

    def __str__(self):
        return f"Partition: name={self.name}, size={self.actual_size} bytes,  unit={self.unit}"

    def pack(self):
        packed_partition = struct.pack(self.FORMAT, self.actual_size, self.name.encode('utf-8'), self.unit.encode('utf-8'))
        return packed_partition

    @classmethod
    def unpack(cls, data):
        unpacked_data = struct.unpack(cls.FORMAT, data)
        ex = {'size': 10, 'path': 'path', 'name': 'name'}
        partition = cls(ex)
        partition.actual_size = unpacked_data[0]
        partition.name = unpacked_data[1].decode('utf-8').strip('\x00')
        partition.unit = unpacked_data[2].decode('utf-8')
            
        return partition
