#include "nnet.h"

int main(int argc, char* argv[])
{
  const char* str = "7 ( i  func 0 0.0  [ ] [ ] ) ( i  func 1 0.0  [ ] [ ] ) ( m relu 2 0.0 [ 0  1 ] [ -0.150428056717 -0.0750720500946 ] ) ( m relu 3 0.0 [ 0  1 ] [ -0.226973056793 -0.62873840332 ] ) ( m relu 4 0.0 [ 0  1 ] [ 0.0121684074402 0.303765773773 ] ) ( m relu 5 0.0 [ 0  1 ] [ -0.777081727982 -0.086953163147 ] ) ( m linear 6 0.0 [ 2  3  4  5 ] [ 0.134516835213 -0.00839650630951 0.637048482895 0.332227468491 ] )";
  nnet_interpreter::Graph G(str);
  std::vector<double> f = std::vector<double>{2.5,-3.1};
  G.setInputs(f);
  std::cout << "value = " << G.calculate() << std::endl;
  return 0;
}
