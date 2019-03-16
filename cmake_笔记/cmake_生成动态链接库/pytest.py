
from pyfunc import sayhello,testfunc,convfunc
import numpy as np
X= [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
K = [[1, 1], [1, 1]]

X_np = np.array(X).astype(np.int32)   #注意参数类型要和c++函数里的参数类型一致
K_np = np.array(K).astype(np.int32)
result = np.zeros(shape=[4,4]).astype(np.int32)

sayhello()
testfunc(X_np,3)
convfunc(X_np,K_np,result,2,2,3,3)