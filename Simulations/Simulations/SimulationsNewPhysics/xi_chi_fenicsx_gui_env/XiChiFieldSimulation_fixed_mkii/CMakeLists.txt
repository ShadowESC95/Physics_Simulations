cmake_minimum_required(VERSION 3.18)
project(XiChiFieldSimulation LANGUAGES CXX)

find_package(Deal.II REQUIRED HINTS /usr/share/deal.II/cmake)

deal_ii_initialize_cached_variables()

add_executable(xichi_sim
  src/main.cc
  src/field_solver.cc
  src/sinusoidal_modulation.cc
  src/pink_noise_generator.cc
)

target_include_directories(xichi_sim PUBLIC
  ${PROJECT_SOURCE_DIR}/include
)

deal_ii_setup_target(xichi_sim)
