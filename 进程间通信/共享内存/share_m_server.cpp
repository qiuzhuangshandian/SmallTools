#include "shared.h"
#include <sys/shm.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <cstdint>
int main(int argc,char *argv[]){
    
    void *shm = NULL;
    shared_st *shared_m;
    int shmid;

    //创建共享内存
    shmid = shmget((key_t)1234,sizeof(shared_st),0666|IPC_CREAT);

    if(shmid == -1){
        fprintf(stderr,"shmget failed\n");
        exit(EXIT_FAILURE);
    }

    //将共享内存连接到当前进程的地址空间
    shm = shmat(shmid,0,0);
    
    if (shm == (void *)-1){
        fprintf(stderr,"shmat failed\n");
        exit(EXIT_FAILURE);
    }

    printf("memory attached at %ld\n",(intptr_t)shm);

    shared_m = (shared_st *) shm;
    shared_m -> written = 0;

    while(1){

        // 只读取数据，不向内存写数据
        if (shared_m -> written == 1){
            printf("your wrote: %s",shared_m->text);
            sleep(1);

            //读完数据将共享字段中的written标志位设成可写（0）
            shared_m -> written = 0;
             
            if(strncmp(shared_m->text,"end",3) == 0){
                break;
            }

        }
        else{   // written 字段为0，其他进程在写
            sleep(1);
        }

    }

    // 把共享内存从当前进程中分离
    if(shmdt(shm) == -1){
        fprintf(stderr,"shmdt failed\n");
    }

    //删除共享内存
    if (shmctl(shmid,IPC_RMID,0) == -1){
        fprintf(stderr,"shmctl (IPC RMID) failed\n");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);


    printf("shmid is %d, \n over!\n",shmid);

}