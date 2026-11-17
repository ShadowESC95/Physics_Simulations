
// File: entropy_modulation_sim.cc
#include <deal.II/base/function.h>
#include <deal.II/base/logstream.h>
#include <deal.II/base/quadrature_lib.h>
#include <deal.II/base/utilities.h>
#include <deal.II/lac/vector.h>
#include <deal.II/lac/full_matrix.h>
#include <deal.II/lac/dynamic_sparsity_pattern.h>
#include <deal.II/lac/sparse_matrix.h>
#include <deal.II/lac/solver_cg.h>
#include <deal.II/lac/precondition.h>
#include <deal.II/lac/sparse_direct.h>
#include <deal.II/grid/tria.h>
#include <deal.II/grid/grid_generator.h>
#include <deal.II/grid/grid_tools.h>
#include <deal.II/dofs/dof_handler.h>
#include <deal.II/dofs/dof_tools.h>
#include <deal.II/fe/fe_q.h>
#include <deal.II/fe/fe_values.h>
#include <deal.II/numerics/data_out.h>
#include <deal.II/numerics/vector_tools.h>
#include <deal.II/numerics/matrix_tools.h>

#include <fstream>
#include <iostream>

namespace EntropicSim
{
  using namespace dealii;

  template <int dim>
  class EntropicModulation
  {
  public:
    EntropicModulation();
    void run();

  private:
    void setup_system();
    void assemble_system();
    void solve();
    void output_results() const;

    Triangulation<dim> triangulation;
    FE_Q<dim>          fe;
    DoFHandler<dim>    dof_handler;

    SparsityPattern      sparsity_pattern;
    SparseMatrix<double> system_matrix;
    Vector<double>       solution;
    Vector<double>       system_rhs;
  };

  template <int dim>
  EntropicModulation<dim>::EntropicModulation()
    : fe(1)
    , dof_handler(triangulation)
  {}

  template <int dim>
  void EntropicModulation<dim>::setup_system()
  {
    GridGenerator::hyper_cube(triangulation, 0, 1);
    triangulation.refine_global(5);

    dof_handler.distribute_dofs(fe);
    DynamicSparsityPattern dsp(dof_handler.n_dofs());
    DoFTools::make_sparsity_pattern(dof_handler, dsp);
    sparsity_pattern.copy_from(dsp);

    system_matrix.reinit(sparsity_pattern);
    solution.reinit(dof_handler.n_dofs());
    system_rhs.reinit(dof_handler.n_dofs());
  }

  template <int dim>
  void EntropicModulation<dim>::assemble_system()
  {
    QGauss<dim>  quadrature_formula(fe.degree + 1);
    FEValues<dim> fe_values(fe, quadrature_formula, update_values | update_gradients |
                                                          update_quadrature_points | update_JxW_values);

    const unsigned int dofs_per_cell = fe.dofs_per_cell;
    FullMatrix<double> cell_matrix(dofs_per_cell, dofs_per_cell);
    Vector<double>     cell_rhs(dofs_per_cell);

    std::vector<types::global_dof_index> local_dof_indices(dofs_per_cell);

    for (const auto &cell : dof_handler.active_cell_iterators())
    {
      cell_matrix = 0;
      cell_rhs = 0;
      fe_values.reinit(cell);

      for (unsigned int q = 0; q < quadrature_formula.size(); ++q)
      {
        for (unsigned int i = 0; i < dofs_per_cell; ++i)
        {
          for (unsigned int j = 0; j < dofs_per_cell; ++j)
            cell_matrix(i, j) += fe_values.shape_grad(i, q) * fe_values.shape_grad(j, q) * fe_values.JxW(q);

          cell_rhs(i) += 1.0 * fe_values.shape_value(i, q) * fe_values.JxW(q); // Placeholder source term
        }
      }

      cell->get_dof_indices(local_dof_indices);
      for (unsigned int i = 0; i < dofs_per_cell; ++i)
      {
        for (unsigned int j = 0; j < dofs_per_cell; ++j)
          system_matrix.add(local_dof_indices[i], local_dof_indices[j], cell_matrix(i, j));
        system_rhs(local_dof_indices[i]) += cell_rhs(i);
      }
    }
  }

  template <int dim>
  void EntropicModulation<dim>::solve()
  {
    SolverControl            solver_control(1000, 1e-12);
    SolverCG<Vector<double>> solver(solver_control);

    solver.solve(system_matrix, solution, system_rhs, PreconditionIdentity());
  }

  template <int dim>
  void EntropicModulation<dim>::output_results() const
  {
    DataOut<dim> data_out;
    data_out.attach_dof_handler(dof_handler);
    data_out.add_data_vector(solution, "solution");
    data_out.build_patches();
    std::ofstream output("solution.vtk");
    data_out.write_vtk(output);
  }

  template <int dim>
  void EntropicModulation<dim>::run()
  {
    setup_system();
    assemble_system();
    solve();
    output_results();
  }
}

int main()
{
  try
  {
    using namespace EntropicSim;
    EntropicModulation<2> simulation;
    simulation.run();
  }
  catch (std::exception &exc)
  {
    std::cerr << std::endl
              << "Exception on processing: " << std::endl
              << exc.what() << std::endl;
    return 1;
  }
  catch (...)
  {
    std::cerr << std::endl
              << "Unknown exception!" << std::endl;
    return 1;
  }

  return 0;
}
