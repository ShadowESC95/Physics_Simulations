#ifndef PINK_NOISE_GENERATOR_H
#define PINK_NOISE_GENERATOR_H

#include <deal.II/dofs/dof_handler.h>
#include <deal.II/lac/vector.h>

template <int dim>
void apply_pink_noise(dealii::DoFHandler<dim> & /*dof_handler*/,
                      dealii::Vector<double> &data);

#endif // PINK_NOISE_GENERATOR_H

