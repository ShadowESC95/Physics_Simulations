import os
from modules.visualizer import load_h5_field, export_vti, show_slice

field = load_h5_field("outputs/E_field.h5")
export_vti(field, out_path="outputs/E_field.vti")
show_slice(field, axis='z', index=32)

