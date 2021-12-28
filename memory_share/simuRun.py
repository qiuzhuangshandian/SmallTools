import mmap
import struct
import pprint
mmap_file = None
type = "15l20I"
##从内存中读取信息，
def read_mmap_info():    
    global mmap_file
    mmap_file.seek(0)
    info_str=[]
    ##把二进制转换为字符串
    #info_str=mmap_file.read().translate(None, b'\x00').decode()
 
    mmap_file.seek(0)
    info_str=mmap_file.read()    
    print((info_str))
    x=struct.unpack(type,info_str)  #将读取的二进制数进行解包注意字节序
    print(x)
    # print(hex(x))

def get_mmap_info():
    global mmap_file
    ##第二个参数1024是设定的内存大小，单位：字节。如果内容较多，可以调大一点
    mmap_file = mmap.mmap(-1, 140, access = mmap.ACCESS_WRITE, tagname = 'Global\\Center1')
    ##读取有效比特数，不包括空比特
    #cnt=mmap_file.read_byte().decode('utf-8')
    
    cnt=mmap_file.read_byte()
    if cnt==0:
        print("Load data to memory")
        #mmap_file = mmap.mmap(0, 1024, access = mmap.ACCESS_WRITE, tagname = 'share_mmap')
        #mmap_file.write(b"This is the test data")
    else :
        print("The data is in memory")
        read_mmap_info()
 

class SimuPolixir:
    def __init__(self) -> None:
        self.centerMmapFile = mmap.mmap(-1, 140, access = mmap.ACCESS_WRITE, tagname = 'Global\\Center1')
        self.pvatMmapFile = mmap.mmap(-1, 48, access = mmap.ACCESS_WRITE, tagname = 'Global\\PVATableShare1')
        self.pvdtMmapFile = mmap.mmap(-1, 48, access = mmap.ACCESS_WRITE, tagname = 'Global\\PVDTableShare1')
        self.pvaMmapFile = mmap.mmap(-1, 4, access = mmap.ACCESS_WRITE, tagname = 'Global\\PvaShare1')
        self.pvdMmapFile = mmap.mmap(-1, 1, access = mmap.ACCESS_WRITE, tagname = 'Global\\PvdShare1')
        self.centerType = "15l20I"
        self.pvtType = "32s3I?s"
        # self.pvaType = "f"
        # self.pvdType = "?"
        self.centerKeys = [
            "SYSTEM_MDL_RUN",
            "SYSTEM_MDL_STEP",
            "SYSTEM_REVIEWPTR",
            "SYSTEM_SAVE_IC",
            "SYSTEM_SAVE_ICFLAG",
            "SYSTEM_LOAD_IC",
            "SYSTEM_LOAD_ICFLAG",
            "SYSTEM_SAVE_SNAP",
            "SYSTEM_SAVE_SNAPFLAG",
            "SYSTEM_LOAD_SNAP",
            "SYSTEM_LOAD_SNAPFLAG",
            "SYSTEM_PVAUSED",
            "SYSTEM_PVDUSED",
            "SYSTEM_GVAUSED",
            "SYSTEM_TAR_ISTEP",
            "SYSTEM_TEMP_VAR"
        ]
        self.center = {
            "SYSTEM_MDL_RUN":None,
            "SYSTEM_MDL_STEP":None,
            "SYSTEM_REVIEWPTR":None,
            "SYSTEM_SAVE_IC":None,
            "SYSTEM_SAVE_ICFLAG":None,
            "SYSTEM_LOAD_IC":None,
            "SYSTEM_LOAD_ICFLAG":None,
            "SYSTEM_SAVE_SNAP":None,
            "SYSTEM_SAVE_SNAPFLAG":None,
            "SYSTEM_LOAD_SNAP":None,
            "SYSTEM_LOAD_SNAPFLAG":None,
            "SYSTEM_PVAUSED":None,
            "SYSTEM_PVDUSED":None,
            "SYSTEM_GVAUSED":None,
            "SYSTEM_TAR_ISTEP":None,
            "SYSTEM_TEMP_VAR":[]
        }

        self.pvtKeyPos = {"tag":[0,32],"a":[32,35],"Used":[35,36],"x":[35,37]}
        self.pvat = {"tag":"","a":[],"Used":None,"x":None}
        self.pvdt = {"tag":"","a":[],"Used":None,"x":None}
        self.pva = None
        self.pvd = None
        self.obsTitles = [
            "30LOAD","30HYA00DU001OUT","30TOTAL-COAL-T/H","30LAB40CT301","30TOTAL-AIR-FLOW","30MSTEAM-FLOW",
            "30HAH10CT609","30LAE12CF101F","30HAH16CT604","30LAE12AA501AI","30HAH21CT604","30LAE11AA501AI",
            "30LAB11CT609","30LAE14CF101F","30HAH16CT610","30LAE14AA501AI","30HAH22CT604","30LAE13AA501AI",
            "30LAB12CT609"
        ]

    def updateCurrentInfo(self):
        self.updateCurrentCenterInfo()
        self.updatePvatInfo()
        self.updatePvdtInfo()
        self.updatePvaInfo()
        self.updatePvdInfo()

    def updatePvatInfo(self):
        self.pvatMmapFile.seek(0)
        length = int(self.center["SYSTEM_PVAUSED"])
        info_str = self.pvatMmapFile.read(length)
        x = struct.unpack(self.pvtType*length,info_str)
        for i,key in enumerate(self.pvtKeys):
            self.pvat[key] = x[self.pvtKeyPos[0]:self.pvtKeyPos[1]]

    def updatePvdtInfo(self):
        self.pvdtMmapFile.seek(0)
        info_str = self.pvdtMmapFile.read()
        x = struct.unpack(self.pvtType,info_str)
        for i,key in enumerate(self.pvtKeys):
            self.pvdt[key] = x[self.pvtKeyPos[0]:self.pvtKeyPos[1]]

    def updatePvaInfo(self):
        self.pvaMmapFile.seek(0)
        length = int(self.center["SYSTEM_PVAUSED"])
        info_str = self.pvaMmapFile.read(length)
        pvaType = length+"f"
        x = struct.unpack(pvaType,info_str)
        self.pva = list(x)

    def updatePvdInfo(self):
        self.pvdMmapFile.seek(0)
        length = int(self.center["SYSTEM_PVDUSED"])
        info_str = self.pvdMmapFile.read(length)
        pvdType = length+"f"
        x = struct.unpack(pvdType,info_str)
        self.pvd = list(x)

    def updateCurrentCenterInfo(self):
        self.centerMmapFile.seek(0)
        info_str = self.centerMmapFile.read()
        x = struct.unpack(self.centerType,info_str)
        for i,key in enumerate(self.centerKeys):
            if key == "SYSTEM_TEMP_VAR":
                self.center[key] = list(x[i:])
                continue
            self.center[key] = x[i]
        # pprint.pprint(self.centerMembers)

    def getAIndex(self, name):
        for i in range(int(self.center["SYSTEM_PVAUSED"])):
            if not self.pvat[i]["Used"]:
                continue
            if self.pvat[i]["tag"] == name:
                return i

    def getAnalogValueByName(self,name:str):
        pass

    def getCurrentObs(self):
        self.updateCurrentInfo()
        output = {}
        for name in self.obsTitles:
            output[name] = self.getAnalogValueByName(name)


    def getCurrentValueAnalog(self, name:str):
        index = getAIndex(name)


    def getCurrentValueDigit(self, name:str):
        pass


    def closeAllMmap(self):
        self.centerMmapFile.close()
        self.pvatMmapFile.close()
        self.pvdtMmapFile.close()
        self.pvaMmapFile.close()
        self.pvdMmapFile.close()


if __name__=="__main__":
    simu = SimuPolixir()
    simu.getCurrentCenterInfo()
