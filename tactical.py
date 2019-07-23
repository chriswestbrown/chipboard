from board import LFPlay, Board
import numpy

class TacticalPlay(LFPlay):
    def tacticalgreedy(self,V):
        s1 = self.countRemoved(V,0)/self.countRed(V,0)
        s2 = self.countRemoved(V,9)/self.countRed(V,9)
        return s2 - s1
    def antitacticalgreedy(self,V):
        return -1*self.tacticalgreedy(V)

class Tester:
    def testStrat(self,N,strat):
        # Tests different strategy vs the greedy strategy, and provides meaningful
        #results
        t = TacticalPlay()
        res = {"greedy": [], "other": []}
        wins = {"greedy":[], "other":[]}

        for i in range(N):
            b = Board(6,140,.4)
            res["greedy"].append(t.playout(b.clone(),t.greedy))
            res["other"].append(t.playout(b.clone(),strat))
            if res["greedy"][i] < res["other"][i]:
                wins["greedy"].append(i)
            else:
                wins["other"].append(i)

        print "other wins: " + str(len(wins["other"]))
        print "greedy wins: " + str(len(wins["greedy"]))
        wavg_rel = sum([res["greedy"][i]/res["other"][i] for i in wins["other"]])/len(wins["other"])
        lavg_rel = sum([res["other"][i]/res["greedy"][i] for i in wins["greedy"]])/len(wins["greedy"])

        wavg_abs = sum([res["greedy"][i]-res["other"][i] for i in wins["other"]])/len(wins["other"])
        lavg_abs = sum([res["other"][i]-res["greedy"][i] for i in wins["greedy"]])/len(wins["greedy"])


        print "When other wins, it is " + str(wavg_rel) + " times better on average, or " + str(wavg_abs) + " points lower on average"
        print "When greedy wins, it is " + str(lavg_rel) + " times better on average, or " + str(lavg_abs) + " points lower on average"
