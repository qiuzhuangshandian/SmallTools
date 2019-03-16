
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

# X_np = np.array(X).astype(np.int32)   #注意参数类型要和c++函数里的参数类型一致
# K_np = np.array(K).astype(np.int32)
# result = np.zeros(shape=[4,4]).astype(np.int32)

#生成二维数组指针双重指针


#调用
# lib.SayHello()
# lib.test(xpp,3)
# lib.SayHello()
# lib.Conv2(filterpp,xpp,resultpp,2,2,3,3)

def sayhello():
      return lib.SayHello()

def testfunc(x,y):

      xpp  = (x.__array_interface__['data'][0] 
      + np.arange(x.shape[0])*x.strides[0]).astype(np.uintp)

      return lib.test(xpp,y)

def convfunc(x,k,r,a,b,c,d):
      xpp  = (x.__array_interface__['data'][0] 
      + np.arange(x.shape[0])*x.strides[0]).astype(np.uintp)
      filterpp = (k.__array_interface__['data'][0] 
            + np.arange(k.shape[0])*k.strides[0]).astype(np.uintp)
      resultpp = (r.__array_interface__['data'][0] 
            + np.arange(r.shape[0])*r.strides[0]).astype(np.uintp)

      return lib.Conv2(filterpp,xpp,resultpp,a,b,c,d)