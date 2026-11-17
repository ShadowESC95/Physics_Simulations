#!/usr/bin/env bash
python modules/export_xtime_series.py --in data/output/xi_chi_u_evolution.xdmf --out data/output --pattern "xi_chi_u_%04d.vtu" --pvd xi_chi_u_series.pvd
