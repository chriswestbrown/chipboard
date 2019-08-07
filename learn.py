from numpy import loadtxt
from keras.layers import Dense
import keras
import numpy
from board import Board, LFPlay
from tactical import TacticalPlay, Tester
import random
import fileinput
import chipboard
import sys
import math
import time

def getParams(param=1):
    epochs = [10,1,5,20,50]
    lr = ([0.001,0.00001,0.01,0.005,0.0001] if param == 1 else [0.001,0.05,0.01,0.005,0.0001])
    ld = [0.8,0.9,0.7,0.6,0.5]
    nb = [400,100,200,800,1600]
    sets = []
    for i in range(len(epochs)):
        for j in range(len(lr)):
            for k in range(len(ld)):
                for l in range(len(nb)):
                    sets.append((epochs[i],lr[j],ld[k],nb[l]))
    return sets

class Learner:
    def __init__(self,index,numFeatures):
        self.num_nodes = 2
        self.model = keras.Sequential()
        self.num_features = numFeatures
        if self.num_features == 4:
            epochs = [10,1,5,20,50]
            lr = [0.001,0.05,0.01,0.005,0.0001]
            ld = [0.8,0.9,0.7,0.6,0.5]
            nb = [400,100,200,800,1600]
            sets = []
            for i in range(len(epochs)):
                for j in range(len(lr)):
                    for k in range(len(ld)):
                        for l in range(len(nb)):
                            sets.append((epochs[i],lr[j],ld[k],nb[l]))
            self.epochs,self.learning_rate,self.learning_decay,self.num_boards = sets[index]
            self.model.add(Dense(1,input_dim=self.num_features,activation='linear',use_bias=False,kernel_initializer='ones'))
            self.total_boards = 10000
        elif self.num_features == 8:
            epochs = [10,1,5,20,50]
            lr = [0.001,0.00001,0.01,0.005,0.0001]
            ld = [0.8,0.9,0.7,0.6,0.5]
            nb = [400,100,200,800,1600]
            sets = []
            for i in range(len(epochs)):
                for j in range(len(lr)):
                    for k in range(len(ld)):
                        for l in range(len(nb)):
                            sets.append((epochs[i],lr[j],ld[k],nb[l]))
            self.epochs,self.learning_rate,self.learning_decay,self.num_boards = sets[index]
            self.model.add(Dense(self.num_nodes,input_dim=self.num_features,activation='relu',kernel_initializer='ones',bias_initializer='ones'))
            self.model.add(Dense(1,activation='linear',use_bias=False,kernel_initializer='ones'))
            self.total_boards = 20000
        else:
            exit()

        self.opt = keras.optimizers.SGD(lr=self.learning_rate,clipvalue=0.5)
        self.model.compile(self.opt,loss='mean_squared_error',metrics=['accuracy'])
        self.player = LFPlay()

    def playFunc(self,V):
        """Creates the correct feature vector and returns the predicted value from the model,
        in the format of a function that can be used in LFPlay
        V: 36 item array returned in the form expected by the functions countRed and countRemoved from Board"""
        features = self.player.adaptFeatures(V)
        res =  self.model.predict(numpy.array([features]))
        return res[0][0]

    def generateData(self,n,kind,X,Y,rand_init,rand_range):
        """Creates a board, plays a semi-random number of steps on it, then stops to consider
        all possible moves and their resulting values and adds them to provided arrays
        n: Number of boards to consider
        kind: Board type (0,1,2)
        X: 2D numpy array that feature vectors will be added to as encountered
        Y: 1D numpy array for score differences to be added to"""

        count = 0
        for a in range(n):
            b = Board(6,140,.4,kind)
            steps = rand_init +random.randint(0,rand_range)
            self.player.play(b,self.playFunc,steps)
            L = self.player.getMovesWithValues(b,self.playFunc)
            for i in range(len(L)):
                for j in range(i+1,len(L)):
                    if L[i][1] != L[j][1]:
                        r1,c1 = L[i][0]
                        r2,c2 = L[j][0]
                        features = self.player.adaptFeatures(numpy.concatenate((self.player.getPosFeatureVector(b,r1,c1),self.player.getPosFeatureVector(b,r2,c2))))
                        result = L[i][1]-L[j][1]
                        X[count] = features
                        Y[count] = result
                        count += 1
        return (X[:count],Y[:count])

    def learnThings(self,kind=2,rand_init=10,rand_range=7):
        """Generates data and then calls model.fit to learn from the collected data. Decreases
        the learning rate by a provided value and tests the current model against greedy after
        each round of genertion/fitting.
        n: Number of times to generate data and then fit
        ep: Epoch number for fitting
        lr_delta: How much to decrease the learning rate by after each iteration
        size: Number of unique boards to consider when generating data
        kind: Board type to create (0,1,2)"""
        for i in range(math.ceil(self.total_boards/self.num_boards)):
            # print("Starting round " + str(i))
            x,y = self.generateData(self.num_boards,kind,numpy.zeros((size**2,4)),numpy.zeros((size**2)),rand_init,rand_range)
            self.model.fit(x,y,epochs=self.epochs,verbose=0)
            self.learning_rate *= self.learning_decay
            self.opt = keras.optimizers.SGD(lr=self.learning_rate)
            self.model.compile(self.opt,loss='mean_squared_error',metrics=['accuracy'])
            # print("Just completed round " + str(i))
            # self.testKnowledge(1000,kind)

    def testKnowledge(self,n,kind):
        """Tests the current model's prediction against greedy
        n: Number of games to play
        kind: Type of board to use when testing (0,1,2)"""
        t = Tester()
        t.testStrat(n,self.playFunc,kind)

    def learnThingsCPP(self,kind=0,rand_init=10,rand_range=7,test_inc=500,file="stdout",weightFile="stdout",testBoards=100):
        """Generates data and then calls model.fit to learn from the collected data. Decreases
        the learning rate by a provided value and tests the current model against greedy after
        each round of genertion/fitting.
        n: Number of times to generate data and then fit
        ep: Epoch number for fitting
        lr_delta: How much to decrease the learning rate by after each iteration
        num_boards:la Number of unique boards to consider when generating data
        kind: Board type to create (0,1,2)"""

        wf = sys.stdout
        f = sys.stdout
        if file != "stdout":
            f = open(file,"w")
        if weightFile != "stdout":
            wf = open(weightFile,"w")

        timeData = open(file+".time", 'w')
        timeData.write("epochs " + str(self.epochs)+ ", learningRate " + str(self.learning_rate) + ", learningDecay" + str(self.learning_decay) + ", numBoardsPerRound" + str(self.num_boards) +"\n")
        timeData.flush()
        boardsPlayed = 0
        boards_until_test = test_inc
        self.chip = chipboard.ChipboardBoost()
        weights = self.getWeightArray()
        genTimeTotal=0
        modelTimeTotal=0
        timeCounter=0
        initialTest = self.chip.testKnowledge(testBoards,weights,self.num_features,self.num_nodes,random.random(),kind)
        f.write("("+str(boardsPlayed)+","+str(initialTest)+"), ")
        wf.write(str(weights)+"\n")
        f.flush()
        wf.flush()
        for i in range(math.ceil(self.total_boards/self.num_boards)):
            x,y = numpy.zeros((self.num_boards*630,self.num_features)),numpy.zeros((self.num_boards*630))
            weights = self.getWeightArray()
            start_time = time.time()
            count = self.chip.generateData(self.num_boards,kind,x,y,rand_init,rand_range,weights,self.num_features,self.num_nodes,random.random())
            generateDataTime = time.time() - start_time
            genTimeTotal = genTimeTotal + generateDataTime
            timeData.write(str(round(generateDataTime,2))+" ")
            timeData.flush()
            x,y = x[:count],y[:count]
            self.model.fit(x,y,epochs=self.epochs,verbose=0)
            modelTime = time.time()-generateDataTime-start_time
            modelTimeTotal = modelTimeTotal + modelTime
            timeCounter = timeCounter + 1
            timeData.write(str(round(modelTime,2))+"\n")
            timeData.flush()
            boardsPlayed += self.num_boards
            if boardsPlayed >= boards_until_test:
                avgScore = self.chip.testKnowledge(testBoards,weights,self.num_features,self.num_nodes,random.random(),kind)
                f.write("("+str(boardsPlayed)+","+str(avgScore)+"), ")
                wf.write(str(weights)+"\n")
                f.flush()
                wf.flush()
                boards_until_test += test_inc
            self.learning_rate *= self.learning_decay
            self.opt = keras.optimizers.SGD(lr=self.learning_rate,clipvalue=0.5)
            self.model.compile(self.opt,loss='mean_squared_error',metrics=['accuracy'])
        f.write("\n")
        f.close()
        wf.close()
        avgModelTime = modelTimeTotal/timeCounter
        avgGenerateTime = genTimeTotal/timeCounter
        timeData.write("avgGenTime " + str(round(avgGenerateTime, 2)) + ", avgModelFitTime " + str(round(avgModelTime, 2)) + "\n")
        timeData.close()

    def testKnowledgeCPP(self,num=10000,boardType=0):
        self.chip = chipboard.ChipboardBoost()
        weights = self.getWeightArray()
        return self.chip.testKnowledge(num,weights,self.num_features,self.num_nodes,random.random(),boardType)

    def generateTestData(self,X,Y,rand_init,rand_range):
        """Creates a board, plays a semi-random number of steps on it, then stops to consider
        all possible moves and their resulting values and adds them to provided arrays
        n: Number of boards to consider
        kind: Board type (0,1,2)
        X: 2D numpy array that feature vectors will be added to as encountered
        Y: 1D numpy array for score differences to be added to"""

        count = 0
        vals = []
        for line in fileinput.input():
            vals = line.rstrip(",\n").split(", ")
        vals.pop()
        for i in range(len(vals)):
            vals[i] = [int(j) for j in vals[i].lstrip("(").rstrip(")").split(",")]
        b = Board(6,140,.4,0,vals)
        steps = rand_init +random.randint(0,rand_range)
        self.player.play(b,self.playFunc,steps)
        L = self.player.getMovesWithValues(b,self.playFunc)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                if L[i][1] != L[j][1]:
                    r1,c1 = L[i][0]
                    r2,c2 = L[j][0]
                    features = self.player.adaptFeatures(numpy.concatenate((self.player.getPosFeatureVector(b,r1,c1),self.player.getPosFeatureVector(b,r2,c2))))
                    result = L[i][1]-L[j][1]
                    X[count] = features
                    Y[count] = result
                    count += 1
        return (X[:count],Y[:count])
    def getWeightArray(self):
        if self.num_features == 8:
            weights = []
            w = self.model.get_weights()
            weights.append(w[0].tolist())
            weights.append(w[1].tolist())
            weights.append(w[2].tolist())
            return weights
        elif self.num_features == 4:
            return self.model.get_weights()[0].tolist()
