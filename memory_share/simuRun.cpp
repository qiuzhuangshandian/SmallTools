// #include "stdafx.h"
#include <iostream>  
#include <windows.h>  
#include <string>
#include <vector>
#include <map>
#include "simuUtils.h"
#include <thread>

HANDLE  ShareMem(char* _name)
{ 
    HANDLE   hMap=NULL;
    hMap = OpenFileMapping(FILE_MAP_WRITE,NULL, _name);
    return  hMap;
}

void detectAction(PolixirSimu& simu)
{
    while(true)
    {
        simu.doActionByPolicy();
        Sleep(100);   //100ms
    }
    
}

int main()
{
    testAllShareMemory();
    checkStructSize();
    PolixirSimu simu;
    simu.init("simu_polixir_obs","simu_polixir_action");
    simu.showCenterInfo();
    auto threadFunc = [&]()->void{
        detectAction(simu);
    };
    std::thread(threadFunc).detach();
    while(true)
    {
        simu.writeDataToShareMemory();
        Sleep(1*1000);
    }
    return 0;
}


