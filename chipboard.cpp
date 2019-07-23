#include <iostream>
#include <vector>
#include <cstdlib>

class Board
{
public:
  Board(int n, int k, double p);
  bool color(int r, int c);
  int height(int r, int c);
  void choose(int r, int c);
  int score();
  void print();
  int dim() { return n; }
private:
  void pop(int r, int c);
  std::vector< std::vector< std::vector<int> > > B;
  double p;
  int n;
};


Board::Board(int n, int k, double p)
{
  this->p = p;
  this->n = n;
  B.resize(n);
  for(auto itr = B.begin(); itr != B.end(); ++itr)
  {
    (*itr).resize(n);
  }

  for(int i = 0; i < k; ++i)
  {
    int r = rand() % n, c = rand() % n;
    bool cr = rand()/double(RAND_MAX) < p;
    B[r][c].push_back(cr);
  }
}

bool Board::color(int r, int c) { return B[r][c].size() == 0 ? 0 : B[r][c].back(); }
int Board::height(int r, int c) { return B[r][c].size(); }
void Board::pop(int r, int c)
{
  if (0 <= r && r < n && 0 <= c && c < n && B[r][c].size() > 0)
    B[r][c].pop_back();
}
void Board::choose(int r, int c)
{
  if (!color(r,c)) { throw std::exception(); }
  pop(r,c); pop(r-1,c); pop(r,c-1); pop(r+1,c); pop(r,c+1);
}
int Board::score()
{
  int s = 0;
  for(int i = 0; i < n; ++i)
    for(int j = 0; j < n; ++j)
    {
      if (color(i,j)) return -1;
      s += height(i,j);
    }
  return s;
}
void Board::print()
{
  for(int i = 0; i < n; ++i)
  {
    for(int j = 0; j < n; ++j)
    {
      std::cout << ' ';
      if (height(i,j) == 0) std::cout << " "; else std::cout << height(i,j);
      std::cout << (color(i,j) ? '*' : ' ');
    }
    std::cout << std::endl;
  }
}

int randplay(Board B) // note: copy!
{
  int N = B.dim(), s = 0;
  while((s = B.score()) < 0)
  {
    std::vector<int> V;
    for(int i = 0; i < N; ++i)
      for(int j = 0; j < N; ++j)
	if (B.color(i,j))
	  V.push_back(N*i + j);
    int k = rand() % V.size();
    int i = V[k]/N, j = V[k] % N;
    B.choose(i,j);
  }
  return s;
}

int dr[] = {0,0,-1,0,+1};
int dc[] = {0,-1,0,+1,0};
bool in(int r, int c, int N) { return 0 <= r && r < N && 0 <= c && c < N; }
int h(Board &B, int r, int c)
{
  int killc = 0, losec = 0;
  for(int i = 0; i <= 4; ++i)
  {
    int rp = r + dr[i], cp = c + dc[i];
    if (in(rp,cp,B.dim()) && B.height(rp,cp))
      killc++;
    if (in(rp,cp,B.dim()) && B.color(rp,cp))
      losec++;
  }
  return killc - losec;
}

int greedyplay(Board B) // note: copy!
{
  int N = B.dim(), s = 0;
  while((s = B.score()) < 0)
  {
    std::vector<int> V;
    for(int i = 0; i < N; ++i)
      for(int j = 0; j < N; ++j)
	if (B.color(i,j))
	  V.push_back(N*i + j);
    int bestk = 0, bests = h(B,V[0]/N,V[0]%N);
    for(int k = 1; k < V.size(); k++)
    {
      int i = V[k]/N, j = V[k] % N;
      int sc = h(B,i,j);
      if (bests < sc) { bests = sc; bestk = k; }
    }      
    B.choose(V[bestk]/N,V[bestk] % N);
  }
  B.print();
  return s;
}

void humanplay(Board B)
{
  int s = -1;
  while(true)
  {
    B.print();
    if ((s = B.score()) >= 0) break;
    int r, c;
    std::cin >> r >> c;
    B.choose(r,c);
  }
  std::cout << "score = " << s << std::endl;
}

int main(int argc, char** argv)
{
  srand(argc > 1 ? atoi(argv[1]) : time(0));
  Board B(6,140,0.4); //-- this seems big enough to make things interesting!
  B.print();
  std::cout << std::endl << "random scores: ";
  for(int i = 0; i < 20; ++i)
    std::cout << randplay(B) << ' ';
  std::cout << std::endl << "************" << std::endl;
  std::cout << greedyplay(B) << std::endl << std::endl;
  humanplay(B);
  return 0;
}
