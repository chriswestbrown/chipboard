import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ChipBoard extends JFrame implements TileListener , ChipBoardMech.UpdateListener {

  Color ctrlPanelColor = new Color(234,248,247);
  Color ctrlPanelColorB = Color.WHITE;
  
  ChipBoardMech gameMech;
  private Random rand2 = new Random();
  JPanel p;
  TButton button;
  CBLabel l1;
  JTextField tf1;
  CBLabel l2;
  JTextField tf2;
  CBLabel l3;
  JTextField tf3;
  CBLabel l4;
  JTextField tf4;

  //-- TileListener stuff
  public void pressed(Tile t) {
    gameMech.makeMove(t.getPos());
  }
  public int numChips(Pos p) { return gameMech.numChips(p); }
  public boolean redTop(Pos p) { return gameMech.redTop(p); }

  //-- UpdateListener stuff
  public void update(ArrayList<Pos> changedPositions, boolean gameOver) {
    int nc = gameMech.numChips(), ne = gameMech.numEmptyStacks();
    tf1.setText(""+nc);
    tf2.setText(""+ne);
    tf3.setText(""+(ne - nc));
    p.repaint();
  }

  //-- Methods to do the work!
  private void setMech(int seed) {
    gameMech = new ChipBoardMech(seed);
    gameMech.addUpdateListener(this);
  }
  
  public ChipBoard(int seed) {
    super();
    setMech(seed);    
    setTitle("Chipboard");
    p = new JPanel(new GridLayout(gameMech.getNr(),gameMech.getNc()));
    for(int i = 0; i < gameMech.getNr(); i++) {
      for(int j = 0; j < gameMech.getNc(); j++)
	p.add(new Tile(i,j,this));
    }
    l1 = new CBLabel("#chips:");
    tf1 = new JTextField("0",3); tf1.setFocusable(false); tf1.setBackground(ctrlPanelColorB);
    l2 = new CBLabel("#empty:");
    tf2 = new JTextField("0",3); tf2.setFocusable(false); tf2.setBackground(ctrlPanelColorB);
    l3 = new CBLabel("score:");
    tf3 = new JTextField("0",3); tf3.setFocusable(false); tf3.setBackground(ctrlPanelColorB);

    l4 = new CBLabel("seed:");
    tf4 = new JTextField("" + gameMech.getSeed(),4); tf3.setFocusable(false);
    tf4.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e) {
	  try {
	    int s = Integer.parseInt(tf4.getText());
	    setMech(s);
	    update(null,false);
	  }catch(Exception ex) { System.out.println("Error!  Bad seed"); }
	}	
      });

    button = new TButton("⚄");

    JPanel ctrlPanel = new JPanel(new FlowLayout());
    ctrlPanel.setBackground(ctrlPanelColor);
    ctrlPanel.add(l3);
    ctrlPanel.add(tf3);
    tf3.setEditable(false);
    ctrlPanel.add(new CBLabel("="));
    ctrlPanel.add(l2);
    ctrlPanel.add(tf2);
    tf2.setEditable(false);
    ctrlPanel.add(new CBLabel("-"));
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
    rbutton.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e) {
	  setMech(gameMech.getSeed());
	  update(null,false);
	}	
      });      
    ctrlPanel.add(rbutton);
    // TButton nbutton = new TButton("🆕");
    // ctrlPanel.add(nbutton);
    
    ctrlPanel.add(l4);
    ctrlPanel.add(tf4);
    
    add(ctrlPanel,BorderLayout.NORTH);
    add(p,BorderLayout.SOUTH);
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    update(null,false);

    button.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e) {
	  
	  if (!gameMech.gameOver()) { makeRandomMove(); }
	}
      });
  }

  public void makeRandomMove() { gameMech.makeMove(gameMech.randomMove(rand2)); }

  //-- MAIN --
  public static void main(String[] args) {
    boolean help = false;
    Integer seed = null;
    int playType = 0; // 0 <- human, 1 <- random playout
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
    if (playType == 0) {
      ChipBoard b = new ChipBoard(seed);
      b.pack();
      b.setVisible(true);
    }
    else {
      ChipBoardMech b = new ChipBoardMech(seed);
      Random rand2 = new Random();
      while(!b.gameOver()) {
	b.makeMove(b.randomMove(rand2));
      }
    }
  }


  static String msgHTML =
    "<b>usage:</b> <code>chipboard [-r|-h|--help]&lt;seed&gt;</code><br>\n" +
    "<br><b>ChipBoard v0.2</b><br>\n" +
    "<ul><li>Each square represents a stack of alternating red/back chips.</li>\n" +
    "<li>The number is the size of the stack, the color is the color of the top chip.</li>\n" +
    "<li>Click on a *red* number to remove the top chip on that square and those adjacent.</li>\n" +
    "<li>Play stops when there are no more red squares.</li>\n" +
    "<li>Score is calculated as: score = #emtpy_stacks - #number_chips_remaining.</li>\n" +
    "<li>Goal: get the highest score you can!</li></ul>\n" +
    "<br><b>Further Info:</b><ul>" +
    "<li><b><code>-r</code></b> option means no GUI, and the system plays random moves until completion.</li>\n" +
    "</ul>";

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
      "\nChipBoard v0.2\n" +
      "Each square represents a stack of alternating red/back chips.\n" +
      "The number is the size of the stack, the color is the color of the top chip.\n" +
      "Click on a *red* number to remove the top chip on that square and those adjacent.\n" +
      "Play stops when there are no more red squares.\n" +
      "Score is calculated as: score = #emtpy_stacks - #number_chips_remaining.\n" +
      "Goal: get the highest score you can!" +
      "\n\nFurther Info:\n" +
      "-r option means no GUI, and the system plays random moves until completion.\n"
 
      ;
    System.out.println(msg);
  }

  
  
}
