
#include <iostream>
#include<stdio.h>

typedef int Dtype;

extern "C"
{
    void Conv2(Dtype **filter, Dtype **arr, Dtype **res, int filterW, int filterH, int arrW, int arrH);
    void SayHello();
    void test(Dtype **in_array, int N);
}

void Conv2(Dtype **filter, Dtype **arr, Dtype **res, int filterW, int filterH, int arrW, int arrH)
{
    int temp;
    for (int i = 0; i < filterH + arrH - 1; i++)
    {   
        for (int j = 0; j < filterW + arrW - 1; j++)
        { 
            temp = 0;
            for (int m = 0; m < filterH; m++)
            {
                for (int n = 0; n < filterW; n++)
                {
                    if ((i - m) >= 0 && (i - m) < arrH && (j - n) >= 0 && (j - n) < arrW)
                    {   
                        temp += filter[m][n] * arr[i - m][j - n];                    
                    }
                }
            }
            res[i][j] = temp;
            // std::cout << temp << " ";
        }
        
    }
    for (int i = 0; i < filterH + arrH - 1; i++)
    {
        for (int j = 0; j < filterW + arrW - 1; j++)
        {
            std::cout << res[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

void SayHello()
{
    std::cout << "Hello!" << std::endl;
}

void test(Dtype **in_array, int N){
    int i,j;
        for(i = 0; i<N; i++){
            for(j = 0; j<N; j++){
                std::cout << in_array[i][j] <<" ";
        }
        printf("\n");
    }
}