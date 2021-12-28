#include "simuRun.h"

void testAllShareMemory()
{

    char* sharedFileName1 = "Global\\PVATableShare1";
    HANDLE hMapFile1 = OpenFileMapping(FILE_MAP_ALL_ACCESS, NULL, sharedFileName1);
    if (hMapFile1) {
        printf("hMapFile1 open success!\n");
        CloseHandle(hMapFile1);
    }
    else{
        printf("hMapFile1 open failed!\n");
    }

    char* sharedFileName2 = "Global\\PVDTableShare1";
    HANDLE hMapFile2 = OpenFileMapping(FILE_MAP_ALL_ACCESS, NULL, sharedFileName2);
    if (hMapFile2) {
        printf("hMapFile2 open success!\n");
        CloseHandle(hMapFile2);
    }
    else{
        printf("hMapFile2 open failed!\n");
    }

    char* sharedFileName3 = "Global\\PvaShare1";
    HANDLE hMapFile3 = OpenFileMapping(FILE_MAP_ALL_ACCESS, NULL, sharedFileName3);
    if (hMapFile3) {
        printf("hMapFile3 open success!\n");
        CloseHandle(hMapFile3);
    }
    else{
        printf("hMapFile3 open failed!\n");
    }

    char* sharedFileName4 = "Global\\PvdShare1";
    HANDLE hMapFile4 = OpenFileMapping(FILE_MAP_ALL_ACCESS, NULL, sharedFileName4);
    if (hMapFile4) {
        printf("hMapFile4 open success!\n");
        CloseHandle(hMapFile4);
    }
    else{
        printf("hMapFile4 open failed!\n");
    }

    printf("all share memory test finish!\n");
}



void doReadTest()
{
    std::vector<std::string> nameList = {
        "30LOAD","30HYA00DU001OUT","30TOTAL-COAL-T/H","30LAB40CT301","30TOTAL-AIR-FLOW","30MSTEAM-FLOW",
        "30HAH10CT609","30LAE12CF101F","30HAH16CT604","30LAE12AA501AI","30HAH21CT604","30LAE11AA501AI",
        "30LAB11CT609","30LAE14CF101F","30HAH16CT610","30LAE14AA501AI","30HAH22CT604","30LAE13AA501AI",
        "30LAB12CT609"
    };
    PolixirSimu simu;
    simu.init("simu_polixir","simu_polixir_action");
    while(true)
    {
        printf("***************************************\n");
        simu.showCenterInfo();
        for(auto& name:nameList)
        {
            float value = simu.getCurrentValueAnalog(name);
            printf("%s value is:[%f]\n",name.c_str(),value);
        }
        printf("***************************************\n");
        Sleep(2*1000);
        
    }
}

void doWriteTest()
{
    std::vector<std::string> nameList = {
        "30LAE12AA501AI","30LAE11AA501AI","30LAE14AA501AI","30LAE13AA501AI"
    };
    PolixirSimu simu;
    simu.init("simu_polixir","simu_polixir_action");
    for(size_t i=0; i< nameList.size(); i++)
    {
        simu.writeAnalogDataByName(nameList[i],float(i));
        printf("%s write value is [%f]\n",nameList[i].c_str(), float(i));

    }
    for(size_t i=0; i< nameList.size(); i++)
    {
        float value = simu.getCurrentValueAnalog(nameList[i]);
        printf("%s read value is [%f]\n",nameList[i].c_str(), value);
        if(abs(value-float(i) < 0.000001))
        {
            printf("%s write sucecess!\n",nameList[i].c_str());
        }
        else
        {
            printf("%s write failed!\n",nameList[i].c_str());
        }
    }
    std::vector<std::string> nameListCheck = {
        "30LOAD","30HYA00DU001OUT","30TOTAL-COAL-T/H","30LAB40CT301","30TOTAL-AIR-FLOW","30MSTEAM-FLOW",
        "30HAH10CT609","30LAE12CF101F","30HAH16CT604","30LAE12AA501AI","30HAH21CT604","30LAE11AA501AI",
        "30LAB11CT609","30LAE14CF101F","30HAH16CT610","30LAE14AA501AI","30HAH22CT604","30LAE13AA501AI",
        "30LAB12CT609"
    };
    printf("***************************************\n");
    simu.showCenterInfo();
    for(auto& name:nameListCheck)
    {
        float value = simu.getCurrentValueAnalog(name);
        printf("%s value is:[%f]\n",name.c_str(),value);
    }
    printf("***************************************\n");
    return;
}

void checkStructSize()
{
    printf("CENTER size is[%zd]\n",sizeof(CENTER)); //140
    printf("PVT size is[%zd]\n",sizeof(PVT));      // 48
    printf("float size is[%zd]\n",sizeof(float));  // 4
    printf("bool size is[%zd]\n",sizeof(bool));    // 1
}


