
## numpy 中二维数字传递给C++函数的方法

## 编译成动态链接库的g++ 命令：
 g++ -o xxxx.so -shared -fPIC xxx.cpp

 ## 使用方法： 关键点
 extern "C"
{
    void Conv2(int **filter, int **arr, int **res, int filterW, int filterH, int arrW, int arrH);
    void SayHello();
}