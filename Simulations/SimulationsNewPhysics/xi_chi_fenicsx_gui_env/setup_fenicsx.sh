#!/bin/bash
# Setup FEniCSx environment using Mambaforge

# 1. Create & activate environment
mamba create -n fenicsx -c conda-forge python=3.10 dolfinx ufl basix petsc petsc4py mpi4py h5py pyvista pyvistaqt meshio cmake ninja openblas -y
eval "$(mamba shell hook --shell bash)"
mamba activate fenicsx

# 2. Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# 3. Verify installed versions
python -c "import dolfinx, ufl, basix; print('dolfinx', dolfinx.__version__, '| ufl', ufl.__version__, '| basix', basix.__version__)"
python -c "import petsc4py, mpi4py; print('petsc4py', petsc4py.__version__, '| mpi4py', mpi4py.__version__)"
