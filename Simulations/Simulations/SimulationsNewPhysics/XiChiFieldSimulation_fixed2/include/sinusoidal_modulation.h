#pragma once
#include <deal.II/lac/vector.h>
#include <deal.II/dofs/dof_handler.h>

template <int dim>
void apply_sinusoidal_modulation(dealii::DoFHandler<dim> &dof_handler,
                                  dealii::Vector<double> &vec,
                                  double amplitude);
