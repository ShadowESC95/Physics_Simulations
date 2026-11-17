#include "pink_noise_generator.h"

template <int dim>
void apply_pink_noise(dealii::DoFHandler<dim> & /*dof_handler*/,
                      dealii::Vector<double> &data)
{
  (void)data; // suppress unused‑variable if stub
  for (unsigned int i = 0; i < data.size(); ++i)
    data[i] = 0.0;
}

