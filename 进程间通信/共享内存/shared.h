#ifndef _shared_h
#define _shared_h

#define TEXT_SIZE 2048

typedef struct shared_use_st{
    int written; // 标志位，0表示可写。非0表示可读
    char text[TEXT_SIZE];
} shared_st;





#endif