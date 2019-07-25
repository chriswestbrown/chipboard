#include <boost/python.hpp>
#include <algorithm>
#include <iostream>
using namespace boost::python;

class Adder
{
private:
  float lower, upper;

public:
  Adder(float lb, float ub) { lower = lb; upper = ub;  }
  ~Adder() { std::cerr << "Adder destroyed!" << std::endl; }
  void setLower(float x) { lower = x; }
  void setUpper(float x) { upper = x; }
  float width() { return upper - lower; }

  // what's interesting about this example is that it is modifying
  // it argument.  For example, if o is a numpy array, we are modifying
  // the values of that array, w/o allocating new memory!
  // Resource: https://wiki.python.org/moin/boost.python/extract
  void map(object o)
  {
    float dlower, dupper;
    dlower = dupper = extract<float>(o[0]);
    for (int i = 1; i < len(o); ++i) {
      float x = extract<float>(o[i]);
      dlower = std::min(dlower,x);
      dupper = std::max(dupper,x); }
    float dw = dupper - dlower, w = width();
    //list seq = extract<list&>(o);
    for (int i = 0; i < len(o); ++i)
      o[i] = (extract<float>(o[i]) - dlower) / dw * w + lower;
  }

  float fdelta(object o)
  {
    return extract<float>(o(upper)) - extract<float>(o(lower));
  }
  
  tuple get() { //tuple and make_tuple are in boost::python
    return make_tuple(lower,upper);
  }
};


BOOST_PYTHON_MODULE(adder)
{
  class_<Adder>("Adder", init<float, float>())
    .def("setA", &Adder::setLower)
    .def("setB", &Adder::setUpper)
    .def("width", &Adder::width)
    .def("map", &Adder::map)
    .def("fdelta", &Adder::fdelta)
    .def("get", &Adder::get)
    ;
}
