import java.util.*;

public class TestA {
  public static void main(String[] args) {
    Integer seed = null;
    for(int i = 0; i < args.length; i++) {
      try {
	seed = Integer.parseInt(args[i]);
      }catch(Exception e) {
	System.out.println("Error!  Can't interpret '" + args[i] +
			   "' as integer seed value.");
	break;
      }
    }
    if (seed == null) {
      System.out.println("Requires seed argument!");
      System.exit(0);
    }

    for(int nc = 100; nc <= 200; nc += 10) {
      double maxSpread = -999999;
      for(int k = 0; k < 100; k++) {
	int xseed = seed + k;
	// Seed 100, best so far: Game over: 10 chips left on Board, 43 moves made 43 empty cells!
	int sum = 0, N = 100000, max = -999999;
	for(int i = 0; i < N; i++) {
	  ChipBoardMech b = new ChipBoardMech(xseed,nc);
	  Random rand2 = new Random();
	  while(!b.gameOver()) {
	    b.makeMove(b.randomMove(rand2));
	  }
	  int s = b.getScore();
	  sum += s;
	  max = s > max ? s : max;
	}
	double ave = (sum/(double)N);
	double spr = max - ave;
	System.out.println( "spread = " + spr + " ave = " + ave + " max = " + max + " xseed = " + xseed);
	if (spr > maxSpread) {
	  maxSpread = spr;
	}
      }
      System.out.println(nc + "\t" + maxSpread);
    }
  }
}
