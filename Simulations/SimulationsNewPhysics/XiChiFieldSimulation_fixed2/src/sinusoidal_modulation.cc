#include "sinusoidal_modulation.h"
#include <cmath>
#include <deal.II/base/numbers.h>

template <int dim>
void apply_sinusoidal_modulation(dealii::DoFHandler<dim> & /*dof_handler*/,
                                 dealii::Vector<double> &data,
                                 double amplitude)
{
  (void)amplitude; // suppress unused‑variable if stub
  const double two_pi = 2.0 * dealii::numbers::PI;
  for (unsigned int i = 0; i < data.size(); ++i)
    data[i] += amplitude * std::sin(two_pi * i / data.size());
}

