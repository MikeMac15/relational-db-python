import os
import struct
def binary_search_idx(idx_file:str,target_idx:int) -> int:
    file_size = struct.calcsize('ii')
    try:
        with open(idx_file, 'rb') as file:
            file.seek(0,os.SEEK_END())
            num_records = file.tell() // file_size

            L,R = 0, num_records-1

            while True:
                M = (L + R) // 2
                chunk = file.read( M * file_size )

                if not chunk: break

                idx,offset = struct.unpack('ii',file_size)

                if idx == target_idx:
                    return offset
                elif idx < target_idx:
                    L = M + 1
                else: 
                    R = M - 1
    except Exception as e:
        print(e)
        return -2