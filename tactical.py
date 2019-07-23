from board import LFPlay, Board
import numpy

class TacticalPlay(LFPlay):
    def tacticalGreedy(self,V):
        """Greedy choice function."""
        s1 = self.countRemoved(V,0)/self.countRed(V,0)
        s2 = self.countRemoved(V,9)/self.countRed(V,9)
        return s2 - s1
    def antitacticalgreedy(self,V):
        return -1*self.tacticalGreedy(V)

class Tester:
    def testStrats(self,N,strats):
        t = TacticalPlay()
        res = {s : [] for s in strats}
        for i in range(N):
            b = Board(6,140,.4)
            for s in strats:
                res[s].append(t.playout(b.clone(),s))
        wins = {s : 0 for s in strats}
        for i in range(N):
            p = [ res[s][i] for s in strats]
            m = min([res[s][i] for s in strats])
            for s in strats:
                if m == res[s][i]:
                    wins[s] += 1
        return wins
