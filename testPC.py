from learn import Learner
import numpy as np
import warnings
warnings.filterwarnings("ignore")


l = Learner(0.001)
a = l.model.get_weights()
a[0][0][0] = .25
a[0][1][0] = .25
a[0][2][0] = .25
a[0][3][0] = .25
a[1][0] = .25
l.model.set_weights(a)
x,y = l.generateTestData(np.zeros((100,4)),np.zeros((100)),10,0)
for i in range(len(x)):
    print(str(str(int(x[i][0]))+", "+str(int(x[i][1]))+", "+str(int(x[i][2]))+", "+str(int(x[i][3]))+"\n"+str(int(y[i]))))
