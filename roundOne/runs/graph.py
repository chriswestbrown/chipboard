from matplotlib import pyplot as plt
import fileinput
import sys


class Data:
    def __init__(self,format,features=4,param=1):
        if param == 1:
            epochs = [10,1,5,20,50]
            lr = [0.001,0.00001,0.01,0.005,0.0001]
            ld = [0.8,0.9,0.7,0.6,0.5]
            nb = [400,100,200,800,1600]
            nodes = [2,4,8,16,32]
            # rands = [(10,7)]

            sets = []
            for i in range(len(epochs)):
                for j in range(len(lr)):
                    for k in range(len(ld)):
                        for l in range(len(nb)):
                            sets.append((epochs[i],lr[j],ld[k],nb[l]))
        elif param == 2:
            epochs = [10,1,5,20,50]
            lr = [0.001,0.05,0.01,0.005,0.0001]
            ld = [0.8,0.9,0.7,0.6,0.5]
            nb = [400,100,200,800,1600]
            nodes = [2,4,8,16,32]
            # rands = [(10,7)]

            sets = []
            for i in range(len(epochs)):
                for j in range(len(lr)):
                    for k in range(len(ld)):
                        for l in range(len(nb)):
                            sets.append((epochs[i],lr[j],ld[k],nb[l]))
        self.data = {}
        self.weights = {}
        for i in range(8):
            for j in range(80):
                try:
                    index = i*80+j
                    self.data[index] = self.readPerfData(format+"_r_"+str(i)+"_"+str(j)+".txt")
                    if features == 4:
                        self.weights[index] = self.read4FWeights(format+"_w_"+str(i)+"_"+str(j)+".txt")
                    if len(self.data[index]) == 0:
                        self.data.pop(index)
                        self.weights.pop(index)

                except:
                    sys.stderr.write("Could not open file "+str(i)+"_"+str(j)+"\n")


    def graphThings(self,list):
        for i in list:
            x = []
            y = []
            for a,b in self.data[i]:
                x.append(a)
                y.append(b)
            plt.plot(x,y,label=sets[i])
        plt.ylabel('Avg Score')
        plt.xlabel('Boards Created')
        plt.legend()
        plt.show()

    def findBestPerformance(self):
        mins = {}
        for i in self.data:
            mins[i] = self.findMinAvg(self.data[i])
        min_index = mins.keys().pop()
        for i in mins:
            if mins[min_index][1]>mins[i][1]:
                min_index = i
        print("The lowest value was from run "+str(min_index)+", which had a value of "+str(mins[min_index][1])+" and weights of "+str(self.weights[min_index][mins[min_index][0]]))
        return mins[min_index]

    def findWhoBeatGreedy(self,ep=epochs,rate=lr,decay=ld,boards=nb):
        ret = []
        for i in self.data.keys():
            e,r,d,b = sets[i]
            if (e in ep) and (r in rate) and (d in decay) and (b in boards):
                if self.findMinAvg(self.data[i])[1] < 37.9:
                    ret.append(i)
        return ret

    def findNoBeatGreedy(self,ep=epochs,rate=lr,decay=ld,boards=nb):
        ret = []
        for i in self.data.keys():
            e,r,d,b = sets[i]
            if (e in ep) and (r in rate) and (d in decay) and (b in boards):
                if self.findMinAvg(self.data[i])[1] > 37.9:
                    ret.append(i)
        return ret


    def readPerfData(self,fname):
        f = open(fname)
        line = f.read()
        vals = []
        vals = line.rstrip(",\n").split(", ")
        vals.pop()
        for i in range(len(vals)):
            vals[i] = [float(j) for j in vals[i].lstrip("(").rstrip(")").split(",")]
        return vals

    def read4FWeights(self,fname):
        f = open(fname)
        line = f.read()
        vals = line.split("\n")
        vals.pop()
        for i in range(len(vals)):
            vals[i] = [float(j.lstrip("[").rstrip("]")) for j in vals[i].split(", ")]
        return vals

    def findMinAvg(self,r):
        min = 0
        for i in range(1,len(r)):
            if r[min][1] > r[i][1]:
                min = i
        return list([min,r[min][1]])

    def findBestParams(self):
        self.bestParams = {}
        #epochs
        ep = {i:0 for i in epochs}
        for r in lr:
            for d in ld:
                for b in nb:
                    data = {i:self.getData(ep=[i],rate=[r],decay=[d],boards=[b]) for i in ep.keys()}
                    mins = {i:self.findMinAvg(self.data[d[0]])[1] for i,d in data.items()}
                    ep[min(mins, key=mins.get)] +=1
        self.bestParams['epochs'] = ep
        #learning rate
        rate = {i:0 for i in lr}
        for e in epochs:
            for d in ld:
                for b in nb:
                    data = {i:self.getData(ep=[e],rate=[i],decay=[d],boards=[b]) for i in rate.keys()}
                    mins = {i:self.findMinAvg(self.data[d[0]])[1] for i,d in data.items()}
                    rate[min(mins, key=mins.get)] +=1
        self.bestParams['rate'] = rate
        #decay
        decay = {i:0 for i in ld}
        for e in epochs:
            for r in lr:
                for b in nb:
                    data = {i:self.getData(ep=[e],rate=[r],decay=[i],boards=[b]) for i in decay.keys()}
                    mins = {i:self.findMinAvg(self.data[d[0]])[1] for i,d in data.items()}
                    decay[min(mins, key=mins.get)] +=1
        self.bestParams['decay'] = decay
        #boards
        boards = {i:0 for i in nb}
        for e in epochs:
            for r in lr:
                for d in ld:
                    data = {i:self.getData(ep=[e],rate=[r],decay=[d],boards=[i]) for i in boards.keys()}
                    mins = {i:self.findMinAvg(self.data[d[0]])[1] for i,d in data.items()}
                    boards[min(mins, key=mins.get)] +=1
        self.bestParams['boards'] = boards



    def getData(self,ep=epochs,rate=lr,decay=ld,boards=nb):
        ret = []
        for i in self.data.keys():
            e,r,d,b = sets[i]
            if (e in ep) and (r in rate) and (d in decay) and (b in boards):
                ret.append(i)
        return ret
