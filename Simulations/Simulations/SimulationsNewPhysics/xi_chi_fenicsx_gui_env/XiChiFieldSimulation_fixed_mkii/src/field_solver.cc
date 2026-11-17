#include "field_solver.h"
#include "initial_conditions.h"
#include "sinusoidal_modulation.h"
#include <deal.II/grid/grid_generator.h>
#include <deal.II/numerics/data_out.h>
#include <fstream>
#include <cmath>

template <int dim>
FieldSolver<dim>::FieldSolver()
  : fe(1),
    dof_handler(triangulation),
    time(0.0),
    time_step_size(1e-3),
    timestep_number(0) {}

template <int dim>
void FieldSolver<dim>::setup_mesh() {
  dealii::GridGenerator::hyper_cube(triangulation,0,1);
  triangulation.refine_global(2);
  dof_handler.distribute_dofs(fe);
  phi.reinit(dof_handler.n_dofs());
  chi.reinit(dof_handler.n_dofs());
  xi.reinit(dof_handler.n_dofs());
  photon_mass.reinit(dof_handler.n_dofs());
  A_mu.reinit(dof_handler.n_dofs());
}

template <int dim>
void FieldSolver<dim>::initialize_fields() {
  apply_pink_noise<dim>(phi);
  apply_sinusoidal_modulation<dim>(dof_handler, chi, 0.1);
  xi    = 0;
  A_mu  = 0;
}

template <int dim>
void FieldSolver<dim>::time_step() {
  // stub: do nothing
}

template <int dim>
void FieldSolver<dim>::update_photon_mass() {
  for (unsigned int i=0; i<photon_mass.size(); ++i)
    photon_mass[i] = 0;
}

template <int dim>
void FieldSolver<dim>::output_results(unsigned int timestep) const {
  dealii::DataOut<dim> out;
  out.attach_dof_handler(dof_handler);
  out.add_data_vector(phi, "phi");
  out.build_patches();
  std::ofstream file("output/fields-"+std::to_string(timestep)+".vtu");
  out.write_vtu(file);
}

template <int dim>
void FieldSolver<dim>::run() {
  setup_mesh();
  initialize_fields();
  for (unsigned int step=0; step<1; ++step) {
    time_step();
    update_photon_mass();
    output_results(step);
  }
}

template class FieldSolver<3>;
