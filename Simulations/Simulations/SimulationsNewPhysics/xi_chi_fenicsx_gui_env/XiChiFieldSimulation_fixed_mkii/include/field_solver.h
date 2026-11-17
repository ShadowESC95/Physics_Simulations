#pragma once

#include <deal.II/grid/tria.h>
#include <deal.II/fe/fe_q.h>
#include <deal.II/dofs/dof_handler.h>
#include <deal.II/base/quadrature_lib.h>
#include <deal.II/lac/vector.h>
#include <deal.II/numerics/data_out.h>
#include "parameters.h"

template <int dim>
class FieldSolver
{
public:
    FieldSolver();
    void run();

private:
    void setup_mesh();
    void initialize_fields();
    void time_step();
    void output_results(unsigned int timestep) const;

    void solve_xi();
    void solve_chi();
    void solve_phi();
    void solve_photon_field();
    void update_photon_mass();

    static constexpr double G2 = parameters::g_squared;
    static constexpr double L1 = parameters::lambda1;
    static constexpr double L2 = parameters::lambda2;
    static constexpr double L3 = parameters::lambda3;
    static constexpr double Lc = parameters::lambda_c;

    dealii::Triangulation<dim> triangulation;
    dealii::FE_Q<dim> fe;
    dealii::DoFHandler<dim> dof_handler;

    dealii::Vector<double> phi, chi, xi;
    dealii::Vector<double> photon_mass, A_mu;

    double time;
    double time_step_size;
    unsigned int timestep_number;
};

extern template class FieldSolver<3>;
