#include <deal.II/base/logstream.h>
#include "field_solver.h"

int main(int argc, char *argv[]){
  dealii::deallog.depth_console(0);
  FieldSolver<3> solver;
  solver.run();
  return 0;
}
