#include "field_solver.h"
#include "sinusoidal_modulation.h"
#include "initial_conditions.h"
#include <deal.II/grid/grid_generator.h>
#include <deal.II/numerics/data_out.h>
#include <fstream>
#include <cstdlib>

template <int dim>
FieldSolver<dim>::FieldSolver()
  : fe(1),
    dof_handler(triangulation),
    time(0.0),
    time_step_size(1e-3),
    timestep_number(0) {}

template <int dim>
void FieldSolver<dim>::setup_mesh() {
  dealii::GridGenerator::hyper_cube(triangulation, 0, 1);
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
  apply_pink_noise<dim>(dof_handler, phi);
  apply_sinusoidal_modulation<dim>(dof_handler, chi, 0.1);
  for (unsigned int i = 0; i < xi.size(); ++i)
    xi[i] = 0;
  for (unsigned int i = 0; i < A_mu.size(); ++i)
    A_mu[i] = 0;
}

template <int dim>
void FieldSolver<dim>::time_step() {
  // stub: no evolution
}

template <int dim>
void FieldSolver<dim>::update_photon_mass() {
  for (unsigned int i = 0; i < photon_mass.size(); ++i)
    photon_mass[i] = 0;
}

template <int dim>
void FieldSolver<dim>::output_results(unsigned int timestep) const {
  (void)std::system("mkdir -p output"); // ignore return code

  dealii::DataOut<dim> data_out;
  data_out.attach_dof_handler(dof_handler);
  data_out.add_data_vector(phi, "phi");
  data_out.add_data_vector(chi, "chi");
  data_out.add_data_vector(xi, "xi");
  data_out.add_data_vector(photon_mass, "photon_mass");
  data_out.add_data_vector(A_mu, "A_mu");
  data_out.build_patches();
  std::ofstream output("output/fields-" + std::to_string(timestep) + ".vtu");
  data_out.write_vtu(output);
}

template <int dim>
void FieldSolver<dim>::run() {
  setup_mesh();
  initialize_fields();
  for (unsigned int step = 0; step < 1; ++step) {
    time_step();
    update_photon_mass();
    output_results(step);
  }
}

template class FieldSolver<3>;
