
import ctypes as ct
import numpy as np
from numpy.ctypeslib import ndpointer
import numpy.ctypeslib as npct

#定义参数类型双重指针
_doublepp = ndpointer(dtype=np.uintp,ndim=1,flags='C')   

#利用numpy离得ctypeslib库导入动态链接库
lib = npct.load_library("mylib2.so","./")

#重定义函数的参数列表
lib.Conv2.argtypes=[_doublepp,_doublepp,_doublepp,ct.c_int,ct.c_int,ct.c_int,ct.c_int]
lib.Conv2.restype = None
lib.test.argtypes = [_doublepp,ct.c_int]
lib.test.restype = None


#自定义numpy类型的数据
X= [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
K = [[1, 1], [1, 1]]
X_np = np.array(X).astype(np.int32)   #注意参数类型要和c++函数里的参数类型一致
K_np = np.array(K).astype(np.int32)
result = np.zeros(shape=[4,4]).astype(np.int32)

#生成二维数组指针双重指针
xpp  = (X_np.__array_interface__['data'][0] 
      + np.arange(X_np.shape[0])*X_np.strides[0]).astype(np.uintp)
filterpp = (K_np.__array_interface__['data'][0] 
      + np.arange(K_np.shape[0])*K_np.strides[0]).astype(np.uintp)
resultpp = (result.__array_interface__['data'][0] 
      + np.arange(result.shape[0])*result.strides[0]).astype(np.uintp)

#调用
lib.SayHello()
lib.test(xpp,3)
lib.SayHello()
lib.Conv2(filterpp,xpp,resultpp,2,2,3,3)


