ChipBoard                     Chris Brown, July 2019

ChipBoard is a toy game that allows us to explore
learning in a challenging situation --- one in which
traditional reinforcement learning isn't a very good
fit.

1) Example using python code:

>>> from board import Board, LFPlay
>>> b = Board(6,140,0.4)
>>> p = LFPlay()
>>> p.playout(b.clone(),p.greedy)
35.0
>>> p.playout(b.clone(),p.antigreedy)
58.0
