#include "nnet.h"
using namespace std;
namespace nnet_interpreter {

  /**
     Parent class that splits off into two usable types: Input(for features) and
     MiddleNode for all other Nodes. Nodes are never actually created.
  */
  class Node{
  public:
    virtual ~Node() { }
    virtual double getValue(double* values){return value;}
    int node_num;
    int value;
  };

  /**
     Subclass of Node, essentially placeholders for values that will come in as
     part of the feature array.
  */
  class InputNode : public Node{
  public:
    InputNode(int nn){
      this->node_num=nn;
    }
  private:
  };

  /**
     Subclass of Node, holds all values required to make calculations: inputs, weights,
     bias, activation function.
  */
  class MiddleNode : public Node{
  public:
    MiddleNode(string f, int nn, vector<int> i, vector<double> w, double b);
    virtual double getValue(double* values);
  private:
    string func;
    vector<int> inputs;
    vector<double>weights;
    double bias;
  };


  //Constructor
  MiddleNode::MiddleNode(string f, int nn, vector<int> i, vector<double> w, double b){
    this->func = f;
    this->node_num = nn;
    this->inputs = i;
    this->weights = w;
    this->bias = b;
  }
  /**
     Uses weights and inputs (as indexes to an array of values), to calculate the dot
     product of weights and values and then adding in bias. Then checks the activation
     function and applies it to the calculated value.
  */
  double MiddleNode::getValue(double* features){
    double ret = 0.0;
    for(int i=0; i<this->inputs.size(); i++){
      ret += features[this->inputs.at(i)]*this->weights.at(i);
    }
    ret += this->bias;
    if(this->func.compare("relu")==0){
      return max(ret,0.0);
    }
    else if(this->func.compare("linear")==0){
      return ret;
    }
    else if(this->func.compare("tanh")==0){
      return std::tanh(ret);
    }
  }

  /**
     Takes an input string in the following format:
     #nodes ( type function node number bias [ inputs ] [ weights ] )...
     Everything must be seperated by a space
     Refer to graphtest.generateGraph() to get a proper graph string
     Parses the input stream, creates the corresponding nodes, and adds to the vector
  */
  Graph::Graph(const char* graph_string){
    stringstream ss(graph_string);
    ss >> num_nodes;
    this->values = new double[this->num_nodes]{0.0};

    for(int i=0; i<num_nodes;i++){
      char temp;
      char func[10];
      char type;
      int nn,ln,nil;
      vector<int> inputs;
      vector<double> weights;
      double bias;

      ss >> temp; // '('s
      ss >> type;
      ss >> func;
      ss >> nn >> bias;
      string n;
      ss >> temp; // '['
      while(ss >> n ){
	if(n.compare("]")==0)
	  break;
	inputs.push_back(stoi(n));
      }
      ss >> temp; // '['
      while(ss >> n ){
	if(n.compare("]")==0)
	  break;
	weights.push_back(stod(n));
      }
      if(type == 'i'){
	this->nodes.push_back(new InputNode(nn));
      }
      else if(type == 'm'){
	this->nodes.push_back(new MiddleNode(func,nn,inputs,weights,bias));
      }
      ss >> temp; // ')'
    }
  }


  /**
     Sets the inputs(features) once they are known. Features will change every run,
     but the weights will stay the same for an entire round.
  */
  void Graph::setInputs(vector<double> features){
    for(int i=0; i<features.size(); i++){
      this->nodes.at(i)->value = features.at(i);
    }
  }
  /**
     Uses memoization to develop the final value that will be returned by the model,
     by systematically calling each node's getValue() function and providing the current
     values if needed, in the order that they appear in the vector
  */
  double Graph::calculate(){
    int i=0;
    while(i<this->nodes.size()){
      this->values[i] = this->nodes.at(i)->getValue(this->values);
      i++;
    }
    return this->values[i-1];
  }

  Graph::~Graph(){
    delete [] values;
    for(int i = 0; i < nodes.size(); ++i)
      delete nodes[i];
  }

}
