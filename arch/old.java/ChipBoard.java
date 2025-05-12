import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ChipBoard extends JFrame implements TileListener {
  public Random rand;
  private static Random rand2 = new Random();
  final int Nr = 7, Nc = 7, k = 150;
  private int count = k, numMovesMade = 0, redShowing = 0, emptyStacks = Nr*Nc;
  CStack[][] B = new CStack[Nr][Nc];
  JPanel p;
  TButton button;
  Integer currentSeed = null;
    
  public class CStack extends ArrayList<Integer> {
    public boolean isEmpty() { return super.size() == 0; }
    public int size() { return super.size(); }
    public int peek() { return get(size() - 1); }
    public void push(int i) {
      if (isEmpty()) { emptyStacks--; }
      int j = isEmpty() ? 0 : peek();
      add(i);
      if (j == 0 && i > 0) redShowing++;
      else if (j > 0 && i == 0) redShowing--;
    }
    public int pop() {
      int sizeBefore = size();
      int i = peek();
      remove(sizeBefore-1);
      if (sizeBefore == 1) { emptyStacks++; }
      int j = isEmpty() || peek() == 0 ? 0 : 1;
      if (i > 0 && j == 0)
	redShowing--;
      else if (i == 0 && j > 0)
	redShowing++;
      return i;
    }
  }
  

  public CStack getS(Pos p) { return B[p.getRow()][p.getCol()]; }
  public int numChips(Pos p) { return getS(p).size(); }
  public boolean redTop(Pos p) {
    CStack s =  getS(p);
    return (s.isEmpty() || s.peek() == 0) ? false : true;
  }
  public boolean remove(Pos p) {
    if (p != null && numChips(p) > 0) {
      //System.out.println("REMOVE: " + p);
      getS(p).pop();
      //System.out.println("      : red showing = " + redShowing );
      count--;
      return true;
    }
    else
      return false;
  }
      
  public void makeMove(Pos p) {
    if (numChips(p) == 0 || !redTop(p))
      System.out.println("Illegal move at: " + p);
    else {
      //System.out.println("BEFOR: red showing = " + redShowing + " count = " + count);
      Pos[] M = { new Pos(0,0),  new Pos(1,0),  new Pos(0,1),  new Pos(-1,0),  new Pos(0,-1)  };
      for(Pos d : M) {
	Pos np = p.plus(d);
	try { if (remove(np))
	    this.p.repaint();
	}catch(ArrayIndexOutOfBoundsException e) { }
      }
      numMovesMade++;
      update();
      //System.out.println("AFTER: red showing = " + redShowing + " count = " + count);
      if (redShowing == 0) {
	System.out.println("Game over: " +
			   "score " + (numberOfEmpty() - count) + ", "	+		   
			   count + " chips left on Board, " +
			   numMovesMade + " moves made, " +
			   numberOfEmpty() + " empty cells!"			   
			   );
	if (noGUI) { System.exit(0); }
      }
    }
  }


  public int numberOfEmpty() {
    int n = 0;
    for(int i = 0; i < Nr; i++)
      for(int j = 0; j < Nc; j++) {
	Pos p = new Pos(i,j);
	n += (numChips(p) == 0 ? 1 : 0);
      }
    return n;
  }
  
  public void pressed(Tile t) {
    makeMove(t.getPos());
  }

  public Pos randomMove() {
    Pos[] A = new Pos[Nr*Nc];
    int n = 0;      
    for(int i = 0; i < Nr; i++)
      for(int j = 0; j < Nc; j++) {
	Pos p = new Pos(i,j);
	if (redTop(p)) { A[n++] = p; }
      }
    return A[rand2.nextInt(n)];
  }

  JLabel l1;
  JTextField tf1;
  JLabel l2;
  JTextField tf2;
  JLabel l3;
  JTextField tf3;
  JLabel l4;
  JTextField tf4;

  public void update() {
    int nc = count, ne = emptyStacks;
    tf1.setText(""+nc);
    tf2.setText(""+ne);
    tf3.setText(""+(ne - nc));
  }
  
  public ChipBoard(int seed) {
    super();
    rand = new Random(seed);	
    currentSeed = seed;
    setTitle("Chipboard");
    // Set up board
    for(int i = 0; i < Nr; i++)
      for(int j = 0; j < Nc; j++)
	B[i][j] = new CStack();
    for(int i = 0; i < k; i++) {
      int r = rand.nextInt(Nr);
      int c = rand.nextInt(Nc);
      int x = rand.nextInt(2);
      Pos p = new Pos(r,c);
      if (numChips(p) == 0)
	B[r][c].push(x);
      else
	B[r][c].push(redTop(p) ? 0 : 1);
    }
    
    p = new JPanel(new GridLayout(Nr,Nc));
    for(int i = 0; i < Nr; i++) {
      for(int j = 0; j < Nc; j++)
	p.add(new Tile(i,j,this));
    }
    l1 = new JLabel("#chips:");
    tf1 = new JTextField("0",3); tf1.setFocusable(false);
    l2 = new JLabel("#empty:");
    tf2 = new JTextField("0",3); tf2.setFocusable(false);
    l3 = new JLabel("score:");
    tf3 = new JTextField("0",3); tf3.setFocusable(false);

    l4 = new JLabel("seed:");
    tf4 = new JTextField("" + currentSeed,4); tf3.setFocusable(false);


    button = new TButton("⚄");

    JPanel ctrlPanel = new JPanel(new FlowLayout());
    ctrlPanel.add(l3);
    ctrlPanel.add(tf3);
    tf3.setEditable(false);
    ctrlPanel.add(new JLabel("="));
    ctrlPanel.add(l2);
    ctrlPanel.add(tf2);
    tf2.setEditable(false);
    ctrlPanel.add(new JLabel("-"));
    ctrlPanel.add(l1);
    ctrlPanel.add(tf1);
    tf1.setEditable(false);
    ctrlPanel.add(button);


    TButton helpButton = new TButton("?");
    helpButton.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e) {
	  makeHelpFrame();
	}	
      });
    ctrlPanel.add(helpButton);

    TButton rbutton = new TButton("⟳");
    ctrlPanel.add(rbutton);
    TButton nbutton = new TButton("🆕");
    ctrlPanel.add(nbutton);
    
    ctrlPanel.add(l4);
    ctrlPanel.add(tf4);
    
    add(ctrlPanel,BorderLayout.NORTH);
    add(p,BorderLayout.SOUTH);
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    update();

    button.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e) {
	  if (redShowing > 0) { makeMove(randomMove()); }
	}
      });
    
    //System.out.println("\nINITIAL: red showing = " + redShowing );
  }

  public boolean noGUI = false;
  
  public static void main(String[] args) {
    boolean help = false;
    Integer seed = null;
    int playType = 0; // 0 <- human, 1 <- random
    for(int i = 0; i < args.length; i++) {
      if (args[i].equals("-r"))
	playType = 1;
      else if (args[i].equals("-h"))
	help = true;
      else if (args[i].equals("--help"))
	help = true;
      else { try {
	  seed = Integer.parseInt(args[i]);
	}catch(Exception e) {
	  help = true;
	  System.out.println("Error!  Can't interpret '" + args[i] +
			     "' as integer seed value.");
	  break;
	}
      }
    }
    if (help || seed == null) {
      printHelp();
      System.exit(0);
    }
    
    // Seed 100, best so far: Game over: 10 chips left on Board, 43 moves made 43 empty cells!
    ChipBoard b = new ChipBoard(seed);
    if (playType == 1) {
      b.noGUI = true;
      while(b.redShowing != 0) {
	b.makeMove(b.randomMove());
      }
      return;
    }
    b.pack();
    b.setVisible(true);

  }


  static String msgHTML =
      "<b>usage:</b> <code>chipboard [-r|-h|--help]&lt;seed&gt;</code><br>\n" +
      "ChipBoard v0.1<br>\n" +
      "<ul><li>Each square represents a stack of alternating red/back chips.</li>\n" +
      "<li>The number is the size of the stack, the color is the color of the top chip.</li>\n" +
      "<li>Click on a *red* number to remove the top chip on that square and those adjacent.</li>\n" +
      "<li>Play stops when there are no more red squares.</li>\n" +
      "<li>Score is calculated as: score = #emtpy_stacks - #number_chips_remaining.</li>\n" +
      "<li>Goal: get the highest score you can!</li></ol>";

  public void makeHelpFrame() {
    JFrame helpFrame = new JFrame();    
    JEditorPane ep = new JEditorPane();
    ep.setContentType("text/html");
    ep.setText(msgHTML);
    helpFrame.add(ep);
    helpFrame.setLocation(400,50);
    helpFrame.pack();
    helpFrame.setVisible(true);
  }
  
  public static void printHelp() {
    String msg =
      "usage: chipboard [-r|-h|--help] <seed>\n" +
      "ChipBoard v0.1\n" +
      "Each square represents a stack of alternating red/back chips.\n" +
      "The number is the size of the stack, the color is the color of the top chip.\n" +
      "Click on a *red* number to remove the top chip on that square and those adjacent.\n" +
      "Play stops when there are no more red squares.\n" +
      "Score is calculated as: score = #emtpy_stacks - #number_chips_remaining.\n" +
      "Goal: get the highest score you can!";
    System.out.println(msg);
  }

  
  
}
