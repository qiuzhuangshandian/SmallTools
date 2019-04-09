/* A simple server in the internet domain using TCP
   The port number is passed as an argument */
//http://www.linuxhowtos.org/c_c++/socket.htm
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>     //contains definitions of a number of data types used in system calls
#include <sys/socket.h>    // includes a number of definitions of structures needed for sockets
#include <netinet/in.h>    //contains constants and structures needed for internet domain addresses.

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
     int sockfd, newsockfd, portno;
     socklen_t clilen;
     char buffer[256];
     struct sockaddr_in serv_addr, cli_addr;
     int n;
     if (argc < 2) {
         fprintf(stderr,"ERROR, no port provided\n");
         exit(1);
     }
     //返回socket文件
     sockfd = socket(AF_INET, SOCK_STREAM, 0);  //address domain of the socket,the type of socket, the protocol It will choose TCP for stream sockets and UDP for datagram sockets
     if (sockfd < 0) 
        error("ERROR opening socket");
     bzero((char *) &serv_addr, sizeof(serv_addr));  //把serv_addr 全部设置成0
     portno = atoi(argv[1]);    //字符串转换成整数
     serv_addr.sin_family = AF_INET;    /* must be AF_INET， contains a code for the address family */
     serv_addr.sin_addr.s_addr = INADDR_ANY;    /* Not used, must be zero */
     serv_addr.sin_port = htons(portno);  //主机字节顺序转换为网络字节顺序  This field contains the IP address of the host
     if (bind(sockfd, (struct sockaddr *) &serv_addr,    //bind() takes three arguments, the socket file descriptor, the address to which is bound, and the size of the address to which it is bound
              sizeof(serv_addr)) < 0) 
              error("ERROR on binding");
     listen(sockfd,5); //The listen system call allows the process to listen on the socket for connections
     clilen = sizeof(cli_addr);
     //The accept() system call causes the process to block until a client connects to the server ，返回通信文件
     newsockfd = accept(sockfd, 
                 (struct sockaddr *) &cli_addr, 
                 &clilen);
     if (newsockfd < 0) 
          error("ERROR on accept");


    // 以上建立好了socket 服务端
    // 以下为自定义功能代码部分

     bzero(buffer,256);
     n = read(newsockfd,buffer,255);   //从socket向buffer读取数据
     if (n < 0) error("ERROR reading from socket");
     printf("Here is the message: %s\n",buffer);
     n = write(newsockfd,"I got your message",18);   //向socket发送数据
     if (n < 0) error("ERROR writing to socket");


     // 自定义功能代码结束
     close(newsockfd);  // 关闭通信文件
     close(sockfd);    //关闭socket
     return 0; 
}