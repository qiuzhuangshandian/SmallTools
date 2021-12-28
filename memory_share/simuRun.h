#ifndef __SIMURUN_H
#define __SIMURUN_H
#include <iostream>  
#include <windows.h>  
#include <string>
#include <vector>
#include <map>


#define DataSize 47

typedef struct{
  long SYSTEM_MDL_RUN;  //模型状态 =1 运行  =0 冻结
  long SYSTEM_MDL_STEP;   //模型运行计数器
  long SYSTEM_REVIEWPTR;  
  long SYSTEM_SAVE_IC;    //初始存储ID
  long SYSTEM_SAVE_ICFLAG;  //初始条件存储标记  每记录一次+1
  long SYSTEM_LOAD_IC;    //初始读取ID
  long SYSTEM_LOAD_ICFLAG; //初始条件读取标记  每读取一次+1
  long SYSTEM_SAVE_SNAP;  //抽点ID
  long SYSTEM_SAVE_SNAPFLAG;//抽点标记  每抽点一次+1
  long SYSTEM_LOAD_SNAP;  //回退ID
  long SYSTEM_LOAD_SNAPFLAG;//回退标记  每回退一次+1
  long SYSTEM_PVAUSED;   //模型A使用空间  或在ISimu帮助画面查看
  long SYSTEM_PVDUSED;   //模型D使用空间  或在ISimu帮助画面查看
  long SYSTEM_GVAUSED;   //模型G使用空间  或在ISimu帮助画面查看
  long  SYSTEM_TAR_ISTEP;   //模型运行目标  用于同步其它模型
  int  SYSTEM_TEMP_VAR[20];
}CENTER;

typedef struct {
    char  tag[32];   //变量名
    int   a[3];
    bool Used;
    char x;
}PVT;

// typedef struct {
//     char  tag[32];   //变量名
//     int   a[3];
//     bool Used;
//     char x;
// }OBSDATA;


HANDLE ShareMem(char* _name);

struct PolixirSimu
{
    PolixirSimu(){}

    bool init(char* shareTag, char* actionTag)
    {
        char* centerAdd = "Global\\Center1";
        centerMapHandle = ShareMem(centerAdd);
        center = (CENTER*)MapViewOfFile(centerMapHandle,FILE_MAP_ALL_ACCESS,0,0,0);

        char* pvatAdd = "Global\\PVATableShare1";
        pvatMapHandle = ShareMem(pvatAdd);
        pvat = (PVT*)MapViewOfFile(pvatMapHandle,FILE_MAP_ALL_ACCESS,0,0,0);

        char* pvdtAdd = "Global\\PVDTableShare1";
        pvdtMapHandle = ShareMem(pvdtAdd);
        pvdt = (PVT*)MapViewOfFile(pvdtMapHandle,FILE_MAP_ALL_ACCESS,0,0,0);

        char* pvaAdd = "Global\\PvaShare1";
        pvaMapHandle = ShareMem(pvaAdd);
        pva = (float*)MapViewOfFile(pvaMapHandle,FILE_MAP_ALL_ACCESS,0,0,0);

        char* pvdAdd = "Global\\PvdShare1";
        pvdMapHandle = ShareMem(pvdAdd);
        pvd = (bool*)MapViewOfFile(pvdMapHandle,FILE_MAP_ALL_ACCESS,0,0,0);

        createShareMemory(shareTag,actionTag);
        clearActionPythonMemory();
        return true;
    }   
    //返回值>0 为变量地址  <0 查找失败
    //模拟量查找
    int GetAIndex(const char *name)
    {   
        if (center == nullptr)
        {
            printf("error! center == nullptr!\n");
            return -1;
        }
        int Index=-1;  
        for(int i=0;i<center->SYSTEM_PVAUSED;i++)
        {  
            if(!pvat[i].Used) continue;
            if(strcmp(pvat[i].tag,name)==0)
            {
                Index=i;
                 break; 
            }
        }
        return Index;
    }
    ///数字量查找
    int GetDIndex(const char *name)  
    {   
        int Index=-1;  
        for(int  i=0;i<center->SYSTEM_PVDUSED;i++)
        {  
            if(!pvdt[i].Used) continue;
            if(strcmp(pvdt[i].tag,name)==0)
            {
                Index=i; 
                break; 
            }
        }
        return Index;
    }

    float getCurrentValueAnalog (const std::string& name)
    {
        int index = GetAIndex(name.c_str());
        if(index < 0)
        {
            printf("find index failied by name:[%s]\n",name.c_str());
            return -1;
        }
        return pva[index];
    }

    bool getCurrentValueDigit(const std::string name)
    {
        int index = GetDIndex(name.c_str());
        if(index < 0)
        {
            printf("find index failied by name:[%s]\n",name.c_str());
            return false;
        }
        return pvd[index];
    }

    bool writeAnalogDataByName(const std::string name, float value)
    {
        int index = GetAIndex(name.c_str());
        if(index>0)
        {
            pva[index] = value;
            return true;
        }
        printf("get analog index by name[%s] error, index is[%d]",name.c_str(), index);
        return false;
    }

    bool writeDigitDataByName(const std::string name, bool value)
    {
        int index = GetDIndex(name.c_str());
        if(index>0)
        {
            pva[index] = value;
            return true;
        }
        printf("get digit index by name[%s] error, index is[%d]",name.c_str(), index);
    }

    void showCenterContent(CENTER* center)
    {
        printf("模型状态 =1 运行  =0 冻结 SYSTEM_MDL_RUN = [%ld]\n",center->SYSTEM_MDL_RUN);
        printf("模型运行计数器SYSTEM_MDL_STEP = [%ld]\n",center->SYSTEM_MDL_STEP);
        printf("SYSTEM_REVIEWPTR = [%ld]\n",center->SYSTEM_REVIEWPTR);

        printf("初始存储ID SYSTEM_SAVE_IC = [%ld]\n",center->SYSTEM_SAVE_IC);
        printf("初始条件存储标记  每记录一次+1 SYSTEM_SAVE_ICFLAG = [%ld]\n",center->SYSTEM_SAVE_ICFLAG);
        
        printf("初始读取ID SYSTEM_LOAD_IC = [%ld]\n",center->SYSTEM_LOAD_IC);
        printf("初始条件读取标记  每读取一次+1 SYSTEM_LOAD_ICFLAG = [%ld]\n",center->SYSTEM_LOAD_ICFLAG);

        printf("抽点ID SYSTEM_SAVE_SNAP = [%ld]\n",center->SYSTEM_SAVE_SNAP);
        printf("抽点标记  每抽点一次+1 SYSTEM_SAVE_SNAPFLAG = [%ld]\n",center->SYSTEM_SAVE_SNAPFLAG);

        printf("回退ID SYSTEM_LOAD_SNAP = [%ld]\n",center->SYSTEM_LOAD_SNAP);
        printf("回退标记  每回退一次+1 SYSTEM_LOAD_SNAPFLAG = [%ld]\n",center->SYSTEM_LOAD_SNAPFLAG);

        printf("模型A使用空间 SYSTEM_PVAUSED = [%ld]\n",center->SYSTEM_PVAUSED);
        printf("模型D使用空间 SYSTEM_PVDUSED = [%ld]\n",center->SYSTEM_PVDUSED);
        printf("模型G使用空间 SYSTEM_GVAUSED = [%ld]\n",center->SYSTEM_GVAUSED);
        printf("模型运行目标 SYSTEM_TAR_ISTEP = [%ld]\n",center->SYSTEM_TAR_ISTEP);
        printf("************SYSTEM_TEMP_VAR begin*************\n");
        for(int i=0; i<20; i++)
        {
            printf("SYSTEM_TEMP_VAR[%d]=[%d]\n",i,center->SYSTEM_TEMP_VAR[i]);
        }
        printf("************SYSTEM_TEMP_VAR end*************\n");

    }

    void showCenterInfo()
    {
        showCenterContent(center);
    }

    CENTER* center{nullptr};
    HANDLE centerMapHandle{nullptr};

    PVT* pvat{nullptr};
    HANDLE pvatMapHandle{nullptr};

    PVT* pvdt{nullptr};
    HANDLE pvdtMapHandle{nullptr};

    float* pva{nullptr}; 
    HANDLE pvaMapHandle{nullptr};
 
    bool*  pvd{nullptr};
    HANDLE pvdMapHandle{nullptr};

    LPVOID lpBase{nullptr};
    float* lpBase_action{nullptr};

    void createShareMemory(char* tagName, char* actionTag)
    {
        HANDLE hMapFile = CreateFileMapping(
            INVALID_HANDLE_VALUE,   // 物理文件句柄
            NULL,   // 默认安全级别
            PAGE_READWRITE,   // 可读可写
            0,   // 高位文件大小
            4*DataSize,   // 低位文件大小
            tagName
            // L"ShareMemorySZHC"   // 共享内存名称
        );
        
        // 映射缓存区视图 , 得到指向共享内存的指针
        lpBase = MapViewOfFile(
            hMapFile,            // 共享内存的句柄
            FILE_MAP_ALL_ACCESS, // 可读写许可
            0,
            0,
            0
        );

        HANDLE hMapFile_action = CreateFileMapping(
            INVALID_HANDLE_VALUE,   // 物理文件句柄
            NULL,   // 默认安全级别
            PAGE_READWRITE,   // 可读可写
            0,   // 高位文件大小
            4*5,   // 低位文件大小
            actionTag
            // L"ShareMemorySZHC"   // 共享内存名称
        );
        
        // 映射缓存区视图 , 得到指向共享内存的指针
        lpBase_action = (float*)MapViewOfFile(
            hMapFile_action,            // 共享内存的句柄
            FILE_MAP_ALL_ACCESS, // 可读写许可
            0,
            0,
            0
        );

    }
    void clearActionPythonMemory()
    {
        float clearData[5]={0,0,0,0,0};
        memcpy((void*)lpBase_action,(const void*)clearData, 5*sizeof(float));
    }

    void checkWriteResult(std::vector<std::string> nameList)
    {
        for(int i=0; i<nameList.size();i++)
        {
            float value = getCurrentValueAnalog(nameList[i]);
            printf("%s value is:[%f]\n",nameList[i].c_str(),value);
        }
    }

    void doActionByPolicy()
    {
        float actData[5];
        for(int i=0; i<5; i++)
        {
            actData[i] = lpBase_action[i];
        }
        if((actData[0]-0) <= 0)
        {
            return;
        }
        printf("*************\n");
        for(int i=0; i<5; i++)
        {
            printf("actData[%d] = [%f]\n",i,actData[i]);
        }
        printf("*************\n");
        // A侧一级减温水调节阀开度,A侧二级减温水调节阀开度,B侧一级减温水调节阀开度,B侧二级减温水调节阀开度
        std::vector<std::string> nameList = {"30LAE12AA501AO2","30LAE11AA501AO2","30LAE14AA501AO2","30LAE13AA501AO2"};
        for(size_t idx=0; idx < nameList.size(); idx++)
        {
            writeAnalogDataByName(nameList[idx],actData[idx+1]);
        }
        float clearData[5]={0,0,0,0,0};
        memcpy((void*)lpBase_action,(const void*)clearData, 5*sizeof(float));
        checkWriteResult(nameList);
        // showCurrentObs();
    }

    void showCurrentObs()
    {
        float obsData[DataSize];
        std::vector<std::string> nameList ={
            "30LOAD", "30HYA00DU001OUT", "30TOTAL-COAL-T/H", "30LAB40CT301", "30TOTAL-AIR-FLOW",
            "30LAB80CF109", "30MSTEAM-FLOW", "30HAH10CT609", "30HAH15CT601", "30HAH16CT601",
            "30HAH16CT602", "30HAH16CT603", "30LAE12AA501AI", "30LAE12CF101F", "30HAH16CT604",
            "30HAH16CT605", "30HAH16CT606", "30HAH21CT601", "30HAH21CT602", "30HAH21CT603",
            "30LAE11AA501AI", "30LAE11CF101F", "30HAH21CT604", "30HAH21CT605", "30HAH21CT606",
            "30LAB11CT601", "30LAB11CT602", "30LAB11CT609",
            "30HAH16CT607", "30HAH16CT608", "30HAH16CT609", "30LAE14AA501AI", "30LAE14CF101F",
            "30HAH16CT610", "30HAH16CT611", "30HAH16CT612", "30HAH22CT601", "30HAH22CT602",
            "30HAH22CT603", "30LAE13AA501AI", "30LAE13CF101F", "30HAH22CT604", "30HAH22CT605",
            "30HAH22CT606", "30LAB12CT601", "30LAB12CT602", "30LAB12CT609"};
        printf("*************************************\n");
        for(int i=0; i<nameList.size();i++)
        {
            float value = getCurrentValueAnalog(nameList[i]);
            printf("%s value is:[%f]\n",nameList[i].c_str(),value);
            obsData[i] = value;
        }
        printf("*************************************\n");
    }

    void writeDataToShareMemory()
    {
        float obsData[DataSize];
        std::vector<std::string> nameList ={
            "30LOAD", "30HYA00DU001OUT", "30TOTAL-COAL-T/H", "30LAB40CT301", "30TOTAL-AIR-FLOW",
            "30LAB80CF109", "30MSTEAM-FLOW", "30HAH10CT609", "30HAH15CT601", "30HAH16CT601",
            "30HAH16CT602", "30HAH16CT603", "30LAE12AA501AI", "30LAE12CF101F", "30HAH16CT604",
            "30HAH16CT605", "30HAH16CT606", "30HAH21CT601", "30HAH21CT602", "30HAH21CT603",
            "30LAE11AA501AI", "30LAE11CF101F", "30HAH21CT604", "30HAH21CT605", "30HAH21CT606",
            "30LAB11CT601", "30LAB11CT602", "30LAB11CT609",
            "30HAH16CT607", "30HAH16CT608", "30HAH16CT609", "30LAE14AA501AI", "30LAE14CF101F",
            "30HAH16CT610", "30HAH16CT611", "30HAH16CT612", "30HAH22CT601", "30HAH22CT602",
            "30HAH22CT603", "30LAE13AA501AI", "30LAE13CF101F", "30HAH22CT604", "30HAH22CT605",
            "30HAH22CT606", "30LAB12CT601", "30LAB12CT602", "30LAB12CT609"};

        std::map<std::string,std::string> someNameMap = {
            {"30LOAD","机组负荷"},{"30HYA00DU001OUT","燃料主控指令"},{"30TOTAL-COAL-T/H","给煤量均值"},{"30LAB40CT301","给水温度"},
            {"30TOTAL-AIR-FLOW","总风量"},
            {"30LAE12AA501AI","A侧一级减温水调节阀开度"},
            {"30LAE11AA501AI","A侧二级减温水调节阀开度"},
            {"30LAE14AA501AI","B侧一级减温水调节阀开度"},
            {"30LAE13AA501AI","B侧二级减温水调节阀开度"},
            {"30HAH21CT601","A侧二级减温入口温度1（屏过出口）"},{"30HAH21CT602","A侧二级减温入口温度2（屏过出口）"},
            {"30HAH21CT603","A侧二级减温入口温度3（屏过出口）"},{"30HAH22CT601","B侧二级减温入口温度1（屏过出口）"},
            {"30HAH22CT602","B侧二级减温入口温度2（屏过出口）"},{"30HAH22CT603","B侧二级减温入口温度3（屏过出口）"},
            {"30LAB11CT601","A侧末级过热器出口温度1"},{"30LAB11CT602","A侧末级过热器出口温度2"},
            {"30LAB12CT601","B侧末级过热器出口温度1"},{"30LAB12CT602","B侧末级过热器出口温度2"},
            {"30LAE12CF101F","A侧一级减温水流量"},{"30LAE11CF101F","A侧二级减温水流量"},
            {"30LAE14CF101F","B侧一级减温水流量"},{"30LAE13CF101F","B侧二级减温水流量"},
            {"30MSTEAM-FLOW","主蒸汽流量"},
            {"30HAH10CT609","汽水分离器出口温度"},
            {"30HAH16CT602","A侧一级减温入口温度2"},
            {"30HAH16CT608","B侧一级减温入口温度2"}
        };
        printf("*************************************\n");
        for(int i=0; i<nameList.size();i++)
        {
            float value = getCurrentValueAnalog(nameList[i]);
            if(someNameMap.find(nameList[i]) != someNameMap.end())
            {
                printf("%s value is:[%f]\n",someNameMap[nameList[i]].c_str(),value);
            }
            // else
            // {
            //     printf("%s value is:[%f]\n",nameList[i].c_str(),value);
            // }
            obsData[i] = value;
        }
        memcpy(lpBase,(const void*)obsData, DataSize*sizeof(float));
        printf("*************************************\n");
    }

    ~PolixirSimu()
    {
        UnmapViewOfFile((void*)center);
        CloseHandle(centerMapHandle);


        UnmapViewOfFile((void*)pvat);
        CloseHandle(pvatMapHandle);

        UnmapViewOfFile((void*)pvdt);
        CloseHandle(pvdtMapHandle);

        UnmapViewOfFile((void*)pva);
        CloseHandle(pvaMapHandle);

        UnmapViewOfFile((void*)pvd);
        CloseHandle(pvdMapHandle);
    }
};

#endif // __SIMURUN_H