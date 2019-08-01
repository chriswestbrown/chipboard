#include <iostream>
#include <vector>
#include <cstdlib>
#include <chrono>
#include <cmath>
#include <vector>
#include <utility>
#include <string>
#include<boost/python.hpp>
#include<limits.h>

using namespace std;
using namespace boost::python;


class Board
{
public:
  Board(int n, int kC, double p, int bt);
  int putChoiceChip(int r, int c);
  int putSurroundingChips(int r, int c);
  double getProb(double n, double p);
  int putChip(int r, int c, bool color, bool choiceChip);
  void removeExtraBottomLayer(int numChipsToRemove);
  bool in(int r, int c, int N);
  bool color(int r, int c);
  int height(int r, int c);
  void choose(int r, int c);
  int score();
  void print();
  void printString();
  int dim() { return n; }
  void setWeights(object w, int nf, int nn);

private:
  int w1, w2, w3, w4, w5;
  void pop(int r, int c);
  std::vector< std::vector< std::vector<int> > > B;
  double p;
  int n;
  int k;
  std::string boardString;
  std::vector<int> bottomRVals;
  std::vector<int> bottomCVals;
  int boardType;
  object weights;
  int num_features, num_nodes;
};

/** int n for size,int k for num chips, double p for probability, int bt for board type
*/
Board::Board(int n, int kC, double p, int bt)
{
  this->p = p;
  this->n = n;
  this->k = kC;
  this->boardType = bt;
  B.resize(n);
  for(auto itr = B.begin(); itr != B.end(); ++itr)
  {
    (*itr).resize(n);
  }

  int i=0;
  while(i<k) {
    int r = rand() % n, c = rand() % n;
    k=k-putChoiceChip(r,c);

  }
  //std::cout<<"integer k winds up being" <<k <<"\n";
  //fflush(stdout);


  int numToRemove = i-k; //number of chips to remove from the bottom
  removeExtraBottomLayer(numToRemove);
}
void Board::setWeights(object w, int nf, int nn){
  this->weights = w;
  this->num_features = nf;
  this->num_nodes = nn;
}


/**If board is type 0, this will always return 1 (bc only one chip is always placed)
  if type 1 or 2, this will return up to 5, depending on how many surrounding chips were placed.
  */
int Board::putChoiceChip(int r, int c) {
  if(this->boardType==0) {
    bool cr = rand()/double(RAND_MAX) < this->p;
    B[r][c].push_back(cr);
    this->boardString.append( "(" + std::to_string(r) + "," + std::to_string(c) + "," + std::to_string(cr) + "), ");
  //  std::cout << "("<<r<<","<<c<<","<<cr<<"),";
    return 1;
  }  else if(this->boardType == -1) {
    //std::cout<<"in this part of the code";
    fflush(stdout);
    int r,c, temp;
    bool cr;
    for(int i=0;i<k;i++) {
      scanf("(%d,%d,%d), ", &r, &c, &temp);
      cr = temp;
      B[r][c].push_back(cr);
  //    std::cout<<"AT position " <<r<<","<<c<<" it prints "<<cr;
      fflush(stdout);
    }
    return this->k;
}else {
    int count=1;
  //  std::cout<<"Placing choice chip at " <<r<<","<<c<<"\n";
    fflush(stdout);
    putChip(r,c,true, true);
    count+=putSurroundingChips(r,c);
    return count;
    //height++ if red, height-- if black


  }
}

void Board::printString() {
  std::cout<< this->boardString;
}

//use expected value to find probability to make sure 40% of chips are red
  double Board::getProb(double n, double p) {
        return -(3.0*pow(n,2.0)+3.0*n-540.0*p +2)/(12.0*pow(n,2.0)-3.0*n-2.0);
}

  /**put chip at r,c with color and whether or not it is a choice-chip*/
  int Board::putChip(int r, int c, bool color, bool choiceChip) {
    int num = 0;
    if(in(r,c,this->n)==true) { //make sure location is ON the board
      B[r][c].push_back(color);
      this->boardString.append("(" + std::to_string(r) + "," + std::to_string(c) + "," + std::to_string(color) + "), ");
      num = 1;
      if(height(r,c) == 1 && choiceChip==false) {
      //  std::cout<<"adding ("<< r<<","<<c<<") to bottom dwelling chips\n";
        this->bottomRVals.push_back(r); //keeping track of the chips on the bottom that we can remove at the end
        this->bottomCVals.push_back(c);
      }
      return num;
    }
  }

  int Board::putSurroundingChips(int r,int c) {
    int count=0;
    if (this->boardType==1) {
      count+=putChip(r-1,c,false, false); //placing chip at r-1, c,  false bc guarenteed black (type1 board, false bc it is NOT a choice tile)
      count+=putChip(r+1,c,false, false);
      count+=putChip(r,c-1,false, false);
      count+=putChip(r,c+1,false, false);
      return count;
    } else if (this->boardType==2) {
      count+=putChip(r-1,c,(rand()/double(RAND_MAX) < getProb(this->n,this->p)), false);
      count+=putChip(r+1,c,(rand()/double(RAND_MAX) < getProb(this->n,this->p)), false);
      count+=putChip(r,c-1,(rand()/double(RAND_MAX) < getProb(this->n,this->p)), false);
      count+=putChip(r,c+1,(rand()/double(RAND_MAX) < getProb(this->n,this->p)), false);
      return count;
    }
  }

void Board::removeExtraBottomLayer(int numChipsToRemove) {
  int i = 0;
  while(i<numChipsToRemove) {
    int rangeSize = bottomRVals.size();
    int index = rand()%rangeSize;
    int x = bottomRVals.at(index);
    int y = bottomCVals.at(index);
    //std::cout<<"x and y to be popped are " << x << "," << y <<"\n";
    B[x][y].erase(B[x][y].begin());
    std::swap(bottomRVals[index], bottomRVals[rangeSize-1]);
    std::swap(bottomCVals[index], bottomCVals[rangeSize-1]);
    bottomRVals.pop_back();
    bottomCVals.pop_back();
    i++;
  }

}


bool Board::in(int r, int c, int N) { return 0 <= r && r < N && 0 <= c && c < N; }
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
  int sum =0;
  for(int i = 0; i < n; ++i)
  {
    for(int j = 0; j < n; ++j)
    {
      std::cout << ' ';
      sum += height(i,j);
      if (height(i,j) == 0) std::cout << " "; else std::cout << height(i,j);
      std::cout << (color(i,j) ? '*' : ' ');
    }
    std::cout << std::endl;
  }
//std::cout<<"Sum of all chips on board: " << sum <<"\n";
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
bool in(int r, int c, int N) { return 0 <= r && r < N && 0 <= c && c < N; };

int dr[] = {0,0,-1,0,+1};
int dc[] = {0,-1,0,+1,0};
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
  // B.print();
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

bool isPotentialLinker(Board B, int r, int c, int r0, int c0) {
  int numRed=0;
  int r1,r2;
  for(int i = 0; i <= 4; ++i)
  {
    int rp = r + dr[i], cp = c + dc[i];
    if (in(rp,cp,B.dim()) && B.color(rp,cp)) {
        r1 = rp;
        r2 = cp;
        numRed++;
      }
    }
    if(numRed==0) {
      return true;

    } else {
      return false;
    }

  }



bool isStrander(Board B, int r, int c, int r0, int c0) {
  int numRed=0;
  int r1,r2;
  for(int i = 0; i <= 4; ++i)
  {
    int rp = r + dr[i], cp = c + dc[i];
    if (in(rp,cp,B.dim()) && B.color(rp,cp)) {
        r1 = rp;
        r2 = cp;
        numRed++;
      }
    }
    if(numRed==1 && B.color(r0,c0)) {
    //  std::cout<<r0<<","<<c0<<" is where something gets stranded"<<endl;
      return true;

    } else {
      return false;
    }

  }

  int drB[] = {+1, 0,-1,-2,-1,0,+1,+2,+1};
  int dcB[] = {-1, -2,-1,0,+1,+2,+1,0,-1};

  int getPotentialFeatures(Board B, int r, int c, int location) {
    int numLinkers = 0;
    int dr0=r+drB[0], dc0=c+dcB[0];
    int dr1=r+drB[1], dc1=c+dcB[1];
    int dr2=r+drB[2], dc2=c+dcB[2];
    int dr3=r+drB[3], dc3=c+dcB[3];
    int dr4=r+drB[4], dc4=c+dcB[4];
    int dr5=r+drB[5], dc5=c+dcB[5];
    int dr6=r+drB[6], dc6=c+dcB[6];
    int dr7=r+drB[7], dc7=c+dcB[7];
    int dr8=r+drB[8], dc8=c+dcB[8];

    switch(location) {
      case 1:
        if(in(dr0,dc0,B.dim()) && isPotentialLinker(B, dr0,dc0, r, c-1)){numLinkers++;}
        if(in(dr1, dc1,B.dim()) && isPotentialLinker(B,dr1, dc1, r, c-1)){numLinkers++;}
        if(in(dr2,dc2,B.dim()) && isPotentialLinker(B,dr2,dc2, r, c-1)){numLinkers++;}
        break;
      case 2:
        if(in(dr2,dc2,B.dim()) && isPotentialLinker(B,dr2,dc2, r-1, c)){numLinkers++;}
        if(in(dr3,dc3,B.dim()) && isPotentialLinker(B,dr3,dc3, r-1, c)){numLinkers++;}
        if(in(dr4,dc4,B.dim()) && isPotentialLinker(B,dr4,dc4, r-1, c)){numLinkers++;}
        break;
      case 3:
        if(in(dr4,dc4,B.dim()) && isPotentialLinker(B,dr4,dc4, r, c+1)){numLinkers++;}
        if(in(dr5,dc5,B.dim()) && isPotentialLinker(B,dr5,dc5, r, c+1)){numLinkers++;}
        if(in(dr6,dc6,B.dim()) && isPotentialLinker(B,dr6,dc6, r, c+1)){numLinkers++;}
        break;
      case 4:
        if(in(dr6,dc6,B.dim()) && isPotentialLinker(B,dr6,dc6, r+1, c)){numLinkers++;}
        if(in(dr7,dc7,B.dim()) && isPotentialLinker(B,dr7,dc7, r+1, c)){numLinkers++;}
        if(in(dr8,dc8,B.dim()) && isPotentialLinker(B,dr8,dc8, r+1, c)){numLinkers++;}
        break;

    }
    return numLinkers;

  }




int getExtFeatures(Board B, int r, int c, int location) {
  int numStranders = 0;
  int dr0=r+drB[0], dc0=c+dcB[0];
  int dr1=r+drB[1], dc1=c+dcB[1];
  int dr2=r+drB[2], dc2=c+dcB[2];
  int dr3=r+drB[3], dc3=c+dcB[3];
  int dr4=r+drB[4], dc4=c+dcB[4];
  int dr5=r+drB[5], dc5=c+dcB[5];
  int dr6=r+drB[6], dc6=c+dcB[6];
  int dr7=r+drB[7], dc7=c+dcB[7];
  int dr8=r+drB[8], dc8=c+dcB[8];

  switch(location) {
    case 1:
      if(in(dr0,dc0,B.dim()) && isStrander(B, dr0,dc0, r, c-1)){numStranders++;}
      if(in(dr1, dc1,B.dim()) && isStrander(B,dr1, dc1, r, c-1)){numStranders++;}
      if(in(dr2,dc2,B.dim()) && isStrander(B,dr2,dc2, r, c-1)){numStranders++;}
      break;
    case 2:
      if(in(dr2,dc2,B.dim()) && isStrander(B,dr2,dc2, r-1, c)){numStranders++;}
      if(in(dr3,dc3,B.dim()) && isStrander(B,dr3,dc3, r-1, c)){numStranders++;}
      if(in(dr4,dc4,B.dim()) && isStrander(B,dr4,dc4, r-1, c)){numStranders++;}
      break;
    case 3:
      if(in(dr4,dc4,B.dim()) && isStrander(B,dr4,dc4, r, c+1)){numStranders++;}
      if(in(dr5,dc5,B.dim()) && isStrander(B,dr5,dc5, r, c+1)){numStranders++;}
      if(in(dr6,dc6,B.dim()) && isStrander(B,dr6,dc6, r, c+1)){numStranders++;}
      break;
    case 4:
      if(in(dr6,dc6,B.dim()) && isStrander(B,dr6,dc6, r+1, c)){numStranders++;}
      if(in(dr7,dc7,B.dim()) && isStrander(B,dr7,dc7, r+1, c)){numStranders++;}
      if(in(dr8,dc8,B.dim()) && isStrander(B,dr8,dc8, r+1, c)){numStranders++;}
      break;

  }
  return numStranders;

}

int* getMoreFeatures(Board B, int r, int c, int r2, int c2){
  int totalChips1 = 0, totalRed1 = 0, numStranders1 = 0,  numLinkers1 =0;
  int totalChips2 = 0, totalRed2 = 0, numStranders2 = 0, numLinkers2 =0;
  for(int i = 0; i <= 4; ++i)
  {
    int rp = r + dr[i], cp = c + dc[i];
    int rp2 = r2 + dr[i], cp2 = c2 + dc[i];
    if (in(rp,cp,B.dim()) && B.height(rp,cp))
      totalChips1++;
    if (in(rp,cp,B.dim()) && B.color(rp,cp)) {
      totalRed1++;
      if(i!=0) {  numStranders1 += getExtFeatures(B, r, c, i);}
    } else {
      numLinkers1 += getPotentialFeatures(B, r, c, i);
    }
    if (in(rp2,cp2,B.dim()) && B.height(rp2,cp2))
      totalChips2++;
    if (in(rp2,cp2,B.dim()) && B.color(rp2,cp2)) {
      totalRed2++;
      if(i!=0) {  numStranders2 += getExtFeatures(B, r2, c2, i);}
    } else {
      numLinkers2 += getPotentialFeatures(B, r2, c2, i);
    }

  }
  // int* returnArr = {totalRed1, totalChips1, totalRed2, totalChips2};
  int * returnArr = new int[8];
  returnArr[0] = totalRed1;
  returnArr[1] = totalChips1;
  returnArr[2] = numStranders1;
  returnArr[3] = numLinkers1;
  returnArr[4] = totalRed2;
  returnArr[5] = totalChips2;
  returnArr[6] =  numStranders2;
  returnArr[7] = numLinkers2;

  // std::cout<<endl;
  return returnArr;

}

 double m(Board &B, int r, int c, int r2, int c2, object weights, int num_features, int num_nodes){

  int * features = getMoreFeatures(B,r,c,r2,c2);
  int sums[num_nodes];
  double returnVal = 0;
  for(int i=0; i<num_features; i++){
    for(int j=0; j<num_nodes; j++){
      sums[j] += extract<double>(weights[0][i][j])*features[i];
    }
  }
  for(int i=0; i<num_nodes; i++){
    sums[i] += extract<double>(weights[1][i]);
    returnVal += std::max(0,sums[i])*extract<double>(weights[2][i][0]);
  }
  return returnVal;
}


int modelPlay(Board B, object weights, int num_features, int num_nodes) // note: copy!
{
  int N = B.dim(), s = 0;
  while((s = B.score()) < 0)
  {
    std::vector<int> V;
    for(int i = 0; i < N; ++i)
      for(int j = 0; j < N; ++j)
	        if (B.color(i,j))
	           V.push_back(N*i + j);

    int bestk = 0;
    for(int k = 1; k < V.size(); k++)
    {
      int k1 = V[bestk]/N, k2 = V[bestk]%N;
      int i = V[k]/N, j = V[k] % N;
      if (m(B,k1,k2,i,j,weights,num_features,num_nodes)>0) {
  //      std::cout<<"We called m here\n";
        bestk = k; }

    }
    B.choose(V[bestk]/N,V[bestk] % N);
  }
//  B.print();
  return s;
}

Board modelPlaySteps(Board B, object weights, int num_features, int num_nodes, int steps ) // note: copy!
{
  int N = B.dim(), s = 0;
  while((s = B.score()) < 0 && steps>0)
  {
    std::vector<int> V;
    for(int i = 0; i < N; ++i)
      for(int j = 0; j < N; ++j)
	        if (B.color(i,j))
	           V.push_back(N*i + j);
    int bestk = 0;
    for(int k = 1; k < V.size(); k++)
    {
      int k1 = V[bestk]/N, k2 = V[bestk]%N;
      int i = V[k]/N, j = V[k] % N;
      if (m(B,k1,k2,i,j,weights,num_features,num_nodes)>0) {
      //  std::cout<<"We called m here\n";
        bestk = k; }

    }
    B.choose(V[bestk]/N,V[bestk] % N);
    steps--;
  }
  // B.print();
  return B;
}

std::pair<int,int> play(Board B,int i, int j, object weights, int num_features, int num_nodes){
  B.choose(i,j);
  int score=modelPlay(B,weights,num_features,num_nodes);
  return std::pair<int,int>(i*B.dim()+j, score);
}

std::vector<std::pair<int,int>> getMovesWithValues(Board B, object weights, int num_features, int num_nodes) // note: copy!
{
  std::vector<std::pair<int,int>> movesWithVals;
  int N = B.dim(), s = 0;
    for(int i = 0; i < N; ++i)
      for(int j = 0; j < N; ++j) {
        if (B.color(i,j)) {
          movesWithVals.push_back(play(B,i,j,weights,num_features,num_nodes));
        }
      }
  return movesWithVals;
}

void printVector(std::vector<std::pair<int,int>> a, int n) {
  for (int i=0;i<a.size();i++) {
    std::cout<<"("<<a[i].first/n<<","<<a[i].first%n<<") has playout value of " <<a[i].second <<"\n";
  }
}

int* getFeatures(Board B, int r, int c, int r2, int c2){
  int totalChips1 = 0, totalRed1 = 0;
  int totalChips2 = 0, totalRed2 = 0;
  for(int i = 0; i <= 4; ++i)
  {
    int rp = r + dr[i], cp = c + dc[i];
    int rp2 = r2 + dr[i], cp2 = c2 + dc[i];
    if (in(rp,cp,B.dim()) && B.height(rp,cp))
      totalChips1++;
    if (in(rp,cp,B.dim()) && B.color(rp,cp))
      totalRed1++;
    if (in(rp2,cp2,B.dim()) && B.height(rp2,cp2))
      totalChips2++;
    if (in(rp2,cp2,B.dim()) && B.color(rp2,cp2))
      totalRed2++;
  }
  // int* returnArr = {totalRed1, totalChips1, totalRed2, totalChips2};
  int * returnArr = new int[4];
  returnArr[0] = totalRed1;
  returnArr[1] = totalChips1;
  returnArr[2] = totalRed2;
  returnArr[3] = totalChips2;

  return returnArr;

}

/**
void generateDataOneRun(Board &B, int x[][4], int *y, int &count, int randInit,
  int randRange, double w1, double w2, double w3, double w4, double w5){
    int steps = randInit + rand()%randRange;
    B = modelPlaySteps(B, w1,w2,w3,w4,w5,randInit);
    std::vector<std::pair<int,int>> movesWithVals = getMovesWithValues(B,w1,w2,w3,w4,w5);
    for(int j=0;j<movesWithVals.size();j++) {
      for(int k=j+1;k<movesWithVals.size();k++) {
        if(movesWithVals[j].second != movesWithVals[k].second) {
          int*features = getFeatures(B, movesWithVals[j].first/6, movesWithVals[j].first%6,
            movesWithVals[k].first/6, movesWithVals[k].first%6);
            for(int l=0; l<4; l++)
            x[count][l] = features[l];
            y[count] = movesWithVals[j].second - movesWithVals[k].second;
            count++;
          }
        }
      }
    }

    int generateData(int numBoards, int boardType, int x[][4], int *y, int randInit,
      int randRange, double w1, double w2, double w3, double w4, double w5){
        int count = 0;
        for(int i=0;i<numBoards;i++) {
          //std::cout << "Board number " << i <<"\n";
          Board B(6,140,.4,boardType);
          std::cout<<"Next Board: ";
          // B.printString();
          std::cout<<"\nfloats w1-w5 are as follows: (" <<w1<< ","<<w2<< ","<<w3<< ","<<w4<< ","<<w5<< ")\n";
          //  B.print();
          generateDataOneRun(B, x, y, count, randInit, randRange, w1,w2,w3,w4,w5);
        }
        return count;

}
*/


class ChipboardBoost
{
  public:
    void generateDataOneRun(Board &B, object x, object y, int &count, int randInit,
      int randRange, object weights, int num_features, int num_nodes){
        int steps = randInit + rand()%randRange;
        B = modelPlaySteps(B, weights, num_features, num_nodes, steps);
        std::vector<std::pair<int,int>> movesWithVals = getMovesWithValues(B,weights, num_features, num_nodes);
        for(int j=0;j<movesWithVals.size();j++) {
          for(int k=j+1;k<movesWithVals.size();k++) {
            if(movesWithVals[j].second != movesWithVals[k].second) {
              int*features = getMoreFeatures(B, movesWithVals[j].first/6, movesWithVals[j].first%6,
                movesWithVals[k].first/6, movesWithVals[k].first%6);
                for(int l=0; l<4; l++)
                x[count][l] = features[l];
                y[count] = movesWithVals[j].second - movesWithVals[k].second;
                count++;
              }
            }
          }
        }

        int generateData(int numBoards, int boardType, object x, object y, int randInit,
          int randRange, object weights, int num_features, int num_nodes, float rand_seed){
            srand(int(double(rand_seed)*UINT_MAX));
            int count = 0;
            for(int i=0;i<numBoards;i++) {
              Board B(6,140,.4,boardType);
              generateDataOneRun(B, x, y, count, randInit, randRange, weights, num_features, num_nodes);
            }
            return count;

        }
        double testKnowledge(int num, object weights, int num_features, int num_nodes,float rand_seed,int boardType){
          srand(int(double(rand_seed)*UINT_MAX));
          int score = 0;
          for(int i=0; i<num; i++){
            Board B(6,140,.4,boardType);
            score += modelPlay(B, weights, num_features, num_nodes);
          }
          double avgScore = (1.0*score)/num;
          return avgScore;
        }

};

BOOST_PYTHON_MODULE(chipboard)
{
  class_<ChipboardBoost>("ChipboardBoost", init<>())
    .def("generateData", &ChipboardBoost::generateData)
    .def("testKnowledge",&ChipboardBoost::testKnowledge);

}



int main(int argc, char** argv) {
/**
  bool genBoard = false, playBoard = false, testGreedy = false;
  if (argc < 2) {
    cerr << "usage: ..." << endl;
    exit(1);
  }
  else if (argv[1] == string("-b")) {
    genBoard = true;
  }
  else if (argv[1] == string("-p")) {
    playBoard = true;
  }
  else if (argv[1] == string("-g")){
    std::cout << "Hi\n";
    testGreedy = true;
  }

  srand(argc > 2 ? atoi(argv[2]) : time(0));
  int sum = 0;

  if (genBoard) {
    Board B(6,140,.4,0);
    B.printString();
}  else if (playBoard) {
    int x[1000][4];
    int y[1000];
    int count = generateData(1, -1, x,  y, 10, 7, std::stod(argv[2]), std::stod(argv[3]), std::stod(argv[4]), std::stod(argv[5]), std::stod(argv[6]));
    for(int i=0;i<count; i++){
      std::cout << x[i][0] << ", " << x[i][1] << ", " << x[i][2] << ", " << x[i][3] << "\n" << y[i] << "\n";
    }
  }
  else if (testGreedy) {
    std::cout <<"HI\n";
    int score = 0;
    for(int i=0; i<10000; i++){
      Board B(6,140,.4,2);
      score += greedyplay(B);
    }
    double avgScore = (1.0*score)/10000;
    std::cout << "The average score for greedy over 10000 runs on a type 2 board is " << avgScore << "\n";
  }
  else {
    // Board A(6, 140, 0.4,0); // 0  for typoe 0
    // Board B(6,140,0.4,1); //1 for type 1
    // Board C(6,140,0.4,2); //2 type 2
    // Board D(6,140,0.4, 0);
    // modelPlaySteps(A, .25, .25, .25, .25, .25,10);
    // printVector(getMovesWithValues(A, .25,.25,.25,.25,.25), 6);
    int x[1000][4];
    int y[1000];
    int count = generateData(1, 0, x,  y, 10, 7, .25, .25, .25, .25, .25);
    for(int i=0;i<count; i++){
      std::cout << x[i][0] << ", " << x[i][1] << ", " << x[i][2] << ", " << x[i][3] << "\n" << y[i] << "\n";
    }
    */
}
  //modelPlay(A, .25, .25, .25, .25, .25);
/**  A.print();
  std::cout<<"\n";
  greedyplay(A);
  std::cout<<"\n*********\n";
  B.print();//-- this seems big enough to make things interesting!
  std::cout<<"\n";
  greedyplay(B);
  std::cout<<"\n*********\n";
  C.print();
  std::cout<<"\n";
  greedyplay(C);
  */
