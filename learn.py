from numpy import loadtxt
from keras.layers import Dense
import keras
import numpy
from board import Board, LFPlay
from tactical import TacticalPlay, Tester
import random

class Learner:
    def __init__(self,l):
        """l denotes the starting value of the lerning rate of the optimizer"""
        self.lr = l
        self.model = keras.Sequential()
        self.model.add(Dense(1,input_dim=4,activation='linear'))
        self.opt = keras.optimizers.SGD(lr=self.lr)
        self.model.compile(self.opt,loss='mean_squared_error',metrics=['accuracy'])
        self.player = LFPlay()

    def playFunc(self,V):
        """Creates the correct feature vector and returns the predicted value from the model,
        in the format of a function that can be used in LFPlay
        V: 36 item array returned in the form expected by the functions countRed and countRemoved from Board"""
        features = self.player.adaptFeatures(V)
        res =  self.model.predict(numpy.array([features]))
        return res[0][0]

    def learnedEquation(self,V):
        """Results from 8 rounds of 'learnThings' run on the model, which beats greedy >50% of the time
        V: 36 item array returned in the form expected by the functions countRed and countRemoved from Board"""
        features = self.player.adaptFeatures(V)
        val = 1.01*features[0]-0.51*features[1]-.99*features[2]+.48*features[3]-.003
        return val

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

    def learnThings(self,n=10,ep=10,lr_delta=.8,size=400,kind=2,rand_init=10,rand_range=7):
        """Generates data and then calls model.fit to learn from the collected data. Decreases
        the learning rate by a provided value and tests the current model against greedy after
        each round of genertion/fitting.
        n: Number of times to generate data and then fit
        ep: Epoch number for fitting
        lr_delta: How much to decrease the learning rate by after each iteration
        size: Number of unique boards to consider when generating data
        kind: Board type to create (0,1,2)"""
        for i in range(n):
            x,y = self.generateData(size,kind,numpy.zeros((size**2,4)),numpy.zeros((size**2)),rand_init,rand_range)
            self.model.fit(x,y,epochs=ep)
            self.lr *= lr_delta
            self.opt = keras.optimizers.SGD(lr=self.lr)
            self.model.compile(self.opt,loss='mean_squared_error',metrics=['accuracy'])
            print("Just completed the "+str(n)+"round")
            self.testKnowledge(1000,kind)

    def testKnowledge(self,n,kind):
        """Tests the current model's prediction against greedy
        n: Number of games to play
        kind: Type of board to use when testing (0,1,2)"""
        t = Tester()
        t.testStrat(n,self.playFunc,kind)
