#include <string>
#include <vector>
#include <stdio.h>
#include <iostream>
#include <sstream>
#include <string.h>
#include <cmath>

namespace nnet_interpreter
{

  class Node;

  /**
     Contains a vector of nodes that make up the graph, indexed in a topological sort.
  */
  class Graph{
  public:
    Graph(const char* graph_string);
    ~Graph();
    void setWeights(char* weight_string);
    void setBias(char* bias_string);
    void print_graph();
    void setInputs(std::vector<double> features);
    double calculate();
    void printValues();
    void clean();
  private:
    std::vector<Node*> nodes;
    double * values;
    int num_nodes;
  };

}

