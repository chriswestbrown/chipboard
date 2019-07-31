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

epochs = [10,1,5,20,50]
lr = [0.001,0.00001,0.01,0.000001,0.0001]
ld = [0.8,0.9,0.7,0.6,0.5]
nb = [400,100,200,800,1600]
# rands = [(10,7)]

sets = []
for i in range(len(epochs)):
    for j in range(len(lr)):
        for k in range(len(ld)):
            for l in range(len(nb)):
                sets.append((epochs[i],lr[j],ld[k],nb[l]))





class Learner:
    def __init__(self,index):
        """l denotes the starting value of the lerning rate of the optimizer"""
        self.epochs,self.learning_rate,self.learning_decay,self.num_boards = sets[index]
        self.model = keras.Sequential()
        self.model.add(Dense(1,input_dim=4,activation='linear'))
        self.opt = keras.optimizers.SGD(lr=self.learning_rate)
        self.model.compile(self.opt,loss='mean_squared_error',metrics=['accuracy'])
        self.player = LFPlay()
        self.totalBoards = 10000

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
        for i in range(math.ceil(self.totalBoards/self.num_boards)):
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

    def learnThingsCPP(self,kind=0,rand_init=10,rand_range=7,test_inc=500,file="stdout",weightFile="stdout",testBoards=1000):
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


        boardsPlayed = 0
        boards_until_test = test_inc
        self.chip = chipboard.ChipboardBoost()
        weights = self.model.get_weights()
        initialTest = self.chip.testKnowledge(testBoards,weights[0][0][0].item(),weights[0][1][0].item(),weights[0][2][0].item(),weights[0][3][0].item(),weights[1][0].item(),random.random(),kind)
        f.write("("+str(boardsPlayed)+","+str(initialTest)+"), ")
        wf.write("("+str(weights[0][0][0])+","+str(weights[0][1][0])+","+str(weights[0][2][0])+","+str(weights[0][3][0])+","+str(weights[1][0])+"), ")
        for i in range(math.ceil(self.totalBoards/self.num_boards)):
            x,y = numpy.zeros((self.num_boards**2,4)),numpy.zeros((self.num_boards**2))
            weights = self.model.get_weights()
            count = self.chip.generateData(self.num_boards,kind,x,y,rand_init,rand_range,weights[0][0][0].item(),weights[0][1][0].item(),weights[0][2][0].item(),weights[0][3][0].item(),weights[1][0].item(),random.random())
            x,y = x[:count],y[:count]
            self.model.fit(x,y,epochs=self.epochs,verbose=0)
            boardsPlayed += self.num_boards
            if boardsPlayed >= boards_until_test:
                avgScore = self.chip.testKnowledge(testBoards,weights[0][0][0].item(),weights[0][1][0].item(),weights[0][2][0].item(),weights[0][3][0].item(),weights[1][0].item(),random.random(),kind)
                f.write("("+str(boardsPlayed)+","+str(avgScore)+"), ")
                wf.write("("+str(weights[0][0][0])+","+str(weights[0][1][0])+","+str(weights[0][2][0])+","+str(weights[0][3][0])+","+str(weights[1][0])+"), ")
                boards_until_test += test_inc
            self.learning_rate *= self.learning_decay
            self.opt = keras.optimizers.SGD(lr=self.learning_rate)
            self.model.compile(self.opt,loss='mean_squared_error',metrics=['accuracy'])
        # f.close()
    def testKnowledgeCPP(self,num=1000,boardType=2):
        weights = self.model.get_weights()
        self.chip.testKnowledge(num,weights[0][0][0].item(),weights[0][1][0].item(),weights[0][2][0].item(),weights[0][3][0].item(),weights[1][0].item(),random.random(),boardType)

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
