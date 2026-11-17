file(REMOVE_RECURSE
  "CMakeFiles/object_lac_inst"
  "affine_constraints.inst"
  "block_sparse_matrix.inst"
  "block_vector.inst"
  "chunk_sparse_matrix.inst"
  "full_matrix.inst"
  "la_parallel_block_vector.inst"
  "la_parallel_vector.inst"
  "lapack_full_matrix.inst"
  "petsc_communication_pattern.inst"
  "precondition_block.inst"
  "read_write_vector.inst"
  "relaxation_block.inst"
  "scalapack.inst"
  "solver.inst"
  "sparse_matrix.inst"
  "sparse_matrix_ez.inst"
  "tensor_product_matrix.inst"
  "trilinos_sparse_matrix.inst"
  "trilinos_vector.inst"
  "vector.inst"
  "vector_memory.inst"
  "vector_memory_release.inst"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/object_lac_inst.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
