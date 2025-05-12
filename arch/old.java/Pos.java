/**
 * class Pos does row/column coordinates exactly how you would
 * expect.
 */
public class Pos
{
  private int row, col;

  /**
   * Constructor.
   */
  public Pos(int r, int c) { row = r; col = c; }

  public Pos plus(Pos p) { return new Pos(row + p.row, col + p.col); }

  /**
   * Gets the row value.
   */
  public int getRow() { return row; }

  /**
   * Gets the column value.
   */
  public int getCol() { return col; }

  /**
   * prints out as string row,col
   */
  public String toString() { return row + "," + col; }

  /**
   * equality predicate for Pos objects 
   */
  public boolean equals(Pos p) { return row == p.row && col == p.col; }
}
