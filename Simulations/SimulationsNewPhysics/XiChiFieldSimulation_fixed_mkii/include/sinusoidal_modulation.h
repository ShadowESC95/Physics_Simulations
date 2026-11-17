#pragma once
#include <deal.II/base/quadrature_lib.h>
#include <deal.II/fe/fe_q.h>
#include <deal.II/fe/fe_values.h>
#include <deal.II/dofs/dof_handler.h>
#include <deal.II/lac/vector.h>

template<int dim>
void apply_sinusoidal_modulation(dealii::DoFHandler<dim> &dof_handler,
                                 dealii::Vector<double> &chi,
                                 double amplitude) {
  chi = 0; // stub implementation
}
