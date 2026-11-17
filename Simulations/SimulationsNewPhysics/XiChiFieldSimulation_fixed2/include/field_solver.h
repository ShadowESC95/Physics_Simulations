#pragma once
#include <deal.II/base/logstream.h>
#include <deal.II/lac/vector.h>
#include <deal.II/dofs/dof_handler.h>
#include <deal.II/fe/fe_q.h>
#include <deal.II/grid/tria.h>
#include <deal.II/base/parameter_handler.h>

template <int dim>
class FieldSolver {
public:
  FieldSolver();
  void run();
private:
  void setup_mesh();
  void initialize_fields();
  void time_step();
  void update_photon_mass();
  void output_results(unsigned int timestep) const;

  dealii::Triangulation<dim> triangulation;
  dealii::FE_Q<dim> fe;
  dealii::DoFHandler<dim> dof_handler;
  dealii::Vector<double> phi, chi, xi, photon_mass, A_mu;
  double time, time_step_size;
  unsigned int timestep_number;
};
