from matplotlib import pyplot as plt
import fileinput

class Data:
    def __init__(self,listOfInterest=list(range(625))):
        self.data = {}
        self.weights = {}
        for i in listOfInterest:
            self.data[i] = self.readPerfData("r"+str(i)+".txt")
            self.weights[i] = self.read4FWeights("w"+str(i)+".txt")

    def graphThings(self):
        for i in self.data:
            x = []
            y = []
            for a,b in self.data[i]:
                x.append(a)
                y.append(b)
            plt.plot(x,y,label=i)
        plt.ylabel('Avg Score')
        plt.xlabel('Boards Created')
        plt.legend()
        plt.show()

    def findBestPerformance(self):
        mins = [self.findMinAvg(i) for i in self.data.values()]
        min_index = 0
        for i in range(1,len(mins)):
            if mins[min_index][1]>mins[i][1]:
                min_index = i
        print("The lowest value was from run "+str(min_index)+", which had a value of "+str(mins[min_index][1])+" and weights of "+str(self.weights[min_index][mins[min_index][0]]))
        return mins[min_index]

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
