cmake_minimum_required(VERSION 3.15)
project(openfoam_bridge)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

pybind11_add_module(openfoam_bridge openfoam_bridge.cpp)
