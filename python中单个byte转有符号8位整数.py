import os,struct
#两种byte转有符号整数分方法，第一种自己从补码到反码到原码一步步转换，第二种利用struct库中的unpack函数
def byte2int8(b):
    num = int.from_bytes(b,"big")
    if (num & 0x80) != 0:          #如果不是正数
        num = -((num-1) ^ 0xff)   #补码-1 ->异或方法按位取反->取相反数 
    return num
def byte2int8_(b):
    # b为字节
    [data] = struct.unpack(">b",b)
    return data
def readv(file = "10008.v30" ):
    size = os.path.getsize(file)
    # print(size)
    fr = open(file,"rb")
    # data = fr.read()
    for i in range(size):
        
        data = byte2int8(fr.read(1))
        if data <0:
            print(i,data,file)
        # print(i,data,file)     
    fr.close
def readv2(file = "10008.v30"):
    size = os.path.getsize(file)
    # print(size)
    fr = open(file,"rb")
    # data = fr.read()
    for i in range(size):
        [data] = struct.unpack(">b",fr.read(1))
        if data <0:
            print(i,data,file)
       
    fr.close

# def readc(file = "10008.v30"):
#     size = os.path.getsize(file)
#     print("size is:",size)
#     fr = open(file,"rb")
#     data = fr.read()
#     for i in range(size):
        
#         if data[i] >127:
#             print(i,ord(int(data[i])),file)
#     fr.close

if __name__ == "__main__":
    filelist = os.listdir("./")
    for file in filelist:
        if file.split(".")[-1] == "v30":
            readv(file) 
        # readc(file)