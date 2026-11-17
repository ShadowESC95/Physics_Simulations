#pragma once
#include <deal.II/lac/vector.h>
#include <deal.II/dofs/dof_handler.h>

template <int dim>
void apply_pink_noise(dealii::DoFHandler<dim> &dof_handler,
                      dealii::Vector<double> &vec);
