import board
import numpy as np
import board as bd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from copy import deepcopy

# This is a random policy function
cv = np.array([-0.97282532, -0.93168917, -0.23118399, -1.38933891, -0.43906541,
       -0.1258715 ,  0.83765416, -0.35845139,  0.82477082,  0.89099675,
       -1.02408064,  0.59475197, -0.28502654, -0.22595154, -0.07003846,
       -0.21726488, -0.0090187 ,  1.10076138,  0.78248877,  0.08002113,
        2.1555003 ,  1.38010408,  0.33106784,  0.67521853,  0.98613633,
        0.63229341,  0.6485757 , -0.89753221, -1.21517067,  0.96324863,
        0.47857789,  1.33496433,  0.34973303,  1.54664488, -0.29372008,
       -0.38834292])

finit = lambda V: np.sum(cv*V)

def generate_data_1(n,k,p,policy_f,rng):
    '''
    Produce data from one board.
    
    Parameters:
    n (int): board is nxn
    k (int): number of chips originally on board
    p      : probability that a given chip is red
    policy_f: the policy function to be used
    rng:      random number generator
    '''
    b = bd.Board(n,k,p)
    lfp = bd.LFPlay()
    score,num_moves = lfp.playout(b.clone(),policy_f)
    num_pre_moves = rng.integers(0,num_moves)
    lfp.play(b,policy_f,num_pre_moves)
    L = lfp.getMovesWithValues(b,policy_f)
    n_L = len(L)
    X = [ ]
    Y = [ ]
    for i in range(n_L):
        for j in range(n_L):
            delta = L[i][1] - L[j][1]
            if delta != 0:
                X.append(
                    np.append(lfp.getPosFeatureVector(b,L[i][0][0],L[i][0][1]),
                                   lfp.getPosFeatureVector(b,L[j][0][0],L[j][0][1])))
                Y.append(delta)
    
    return X, Y

def createData(num_iters,policy,rng):
    X = []
    Y = []
    for i in range(num_iters):
        X1,Y1 = generate_data_1(6,140,0.4,policy,rng)
        if (len(Y1) > 0):        
            for i in range(len(X1)):
                for j in range(abs(int(Y1[i]))):
                    X.append(X1[i])
                    Y.append(Y1[i])
    #return X,Y
    return np.array(X), np.array(Y)


def iter(policy,rng,datasize):    
    X,y = createData(datasize,policy,rng)
    lfp = bd.LFPlay()
    Xa = np.array(list(map(lfp.adaptFeatures,X)))
    nnmoda = MLPClassifier(alpha=1e-4, hidden_layer_sizes=(5,5,5,2), learning_rate_init=0.005, random_state=rng.integers(0,999999))
    ys = np.sign(y)
    nnmoda.fit(Xa, ys)
    print(nnmoda.loss_curve_)
    return lambda V: nnmoda.predict([lfp.adaptFeatures(V)])[0]

## NOTES ##
# without warm restart, after four iterations
# we got the following (over 200 eval games)
# greedy  finit after1 after2 after3 after4
# [7309.  8612.  7618.  7147.  7343.  8591.]
# note that finit is a random linear playing
# function based on the original features.
# The learned function use the "adaptedFeatures".
# An option is to duplicate entries numbered by
# how often they appear  When I tried here's what
# I got.
# [7477. 8433. 8065. 7278. 8063. 8385.]

#    nnmoda = MLPClassifier(alpha=1e-4, hidden_layer_sizes=(5,5,5,2), warm_start = true, learning_rate_init=0.005, random_state=rng.integers(0,999999))
def iterWarm(policy,rng,datasize,classifier):    
    X,y = createData(datasize,policy,rng)
    lfp = bd.LFPlay()
    Xa = np.array(list(map(lfp.adaptFeatures,X)))

    ys = np.sign(y)
    classifier.fit(Xa, ys)
    nncopy = deepcopy(classifier)
    return lambda V: nncopy.predict([lfp.adaptFeatures(V)])[0]
