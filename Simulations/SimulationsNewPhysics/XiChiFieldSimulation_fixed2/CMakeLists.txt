cmake_minimum_required(VERSION 3.1)
project(XiChiFieldSimulation)

find_package(deal.II REQUIRED HINTS ${DEAL_II_DIR} /usr/share/cmake/deal.II)
deal_II_initialize_cached_variables()

add_executable(xichi_sim
  src/main.cc
  src/field_solver.cc
  src/pink_noise_generator.cc
  src/sinusoidal_modulation.cc
)

target_include_directories(xichi_sim PRIVATE
  ${CMAKE_SOURCE_DIR}/include
)

deal_II_setup_target(xichi_sim)
