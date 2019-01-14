import os

def byte2int8(num):
    if (num & 0x80) != 0:          #如果不是正数
        num = -((num-1) ^ 0xff)   #补码-1 ->异或方法按位取反->取相反数 
    return num

def readv(file = "10008.v30" ):
    size = os.path.getsize(file)
    # print(size)
    fr = open(file,"rb")
    # data = fr.read()
    for i in range(size):
        
        data = byte2int8(int.from_bytes(fr.read(1),'big'))
      
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