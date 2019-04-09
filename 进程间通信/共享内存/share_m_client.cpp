
#include "shared.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <cstdint>
#include <unistd.h>
#include <cstring>

int main(int arc, char *argv[])
{
    void *shm = NULL;
    shared_st *shared = NULL;
    char buff[200];

    int shmid;
    shmid = shmget((key_t)1234, sizeof(shared_st), 0666 | IPC_CREAT);
    if (shmid == -1)
    {
        fprintf(stderr, "shmget failed\n");
        exit(EXIT_FAILURE);
    }

    shm = shmat(shmid, (void *)0, 0);
    if (shm == (void *)-1)
    {
        fprintf(stderr, "shmat failed\n");
        exit(EXIT_FAILURE);
    }
    printf("Memory attched at %ld\n", (intptr_t)shm);

    shared = (shared_st *)shm;

    while(1)
    {
        while (shared->written == 1)  //有进程在读取数据
        {
            sleep(1);
            printf("waitting...\n");
        }

        //先写 再将标志位设为读（1）
        printf("enter some text: ");
        fgets(buff, 199, stdin);
        strncpy(shared->text, buff, 199);

        shared->written = 1;

        // 输入了end，退出循环（程序）
        if (strncmp(buff, "end", 3) == 0)
        {
            break;
        }
    }
    if (shmdt(shm) == -1)
    {
        fprintf(stderr, "shmdt failed\n");
        exit(EXIT_FAILURE);
    }
    sleep(2);
    exit(EXIT_SUCCESS);
}
