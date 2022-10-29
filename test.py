import os
from libs.conf import *

def main():
    path = "./datas/data_1666766328.txt"
    
    fid = open(path,'rb')
    
    buffer = bytes()
    while True:
        tmp = fid.read(1024)
        if not tmp:
            break
        buffer = buffer + tmp
        index = buffer.find(flag)
        print("buffer len:{},flag index:{}".format(len(buffer),index))
        if index == -1:
            continue
        else:
            buffer = buffer[index+flag_size:]
            
if __name__ == "__main__":
    main()