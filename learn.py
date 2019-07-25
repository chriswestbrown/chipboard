#Steps:
#       1. Build Model
#       2. Construct optimizer
#       3. Compile model
#       4. Model fit(features, result)


from numpy import loadtxt
from keras.layers import Dense
import keras
import numpy
from board import Board, LFPlay
from tactical import TacticalPlay, Tester
import random

class Learner:
    def __init__(self,l):
        self.lr = l
        self.model = keras.Sequential()
        self.model.add(Dense(1,input_dim=4,activation='linear'))
        self.opt = keras.optimizers.SGD(lr=self.lr)
        self.model.compile(self.opt,loss='mean_squared_error',metrics=['accuracy'])
        self.player = LFPlay()


    def getPrediction(self,arr):
        return self.model.predict(arr)

    def fit(self,x,y,e):
        self.model.fit(x,y,epochs=e)

    def playFunc(self,V):
        features = self.player.adaptFeatures(V)
        res =  self.model.predict(numpy.array([features]))
        return res[0][0]

    def generateData(self,n,kind,X,Y):
        count = 0
        for a in range(n):
            b = Board(6,140,.4,kind)
            steps = 10 +random.randint(0,7)
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

    def learnThings(self,n=10,ep=10,lr_delta=.8,size=400,kind=2):
        for i in range(n):
            x,y = self.generateData(size,kind,numpy.zeros((size**2,4)),numpy.zeros((size**2)))
            self.fit(x,y,ep)
            self.lr *= lr_delta
            self.opt = keras.optimizers.SGD(lr=self.lr)
            self.model.compile(self.opt,loss='mean_squared_error',metrics=['accuracy'])

    def testKnowledge(self,n,kind):
        t = Tester()
        t.testStrat(n,self.playFunc,kind)
