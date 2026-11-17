# visual/exascale_render.py
from paraview.simple import *
xi_reader = OpenDataFile("xi_fields/*.vti")
RenderView1 = GetRenderView()
RenderView1.LODThreshold = 1e18  # 1 exabyte
SaveAnimation("field_evolution.mp4")
