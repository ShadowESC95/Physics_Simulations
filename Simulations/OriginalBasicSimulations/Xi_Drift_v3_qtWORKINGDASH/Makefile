.PHONY: viewer render phase clean

viewer:
	python3 visual/qt_field_viewer3d.py

render:
	python3 visual/yt_volume_view.py data/xi_yt_dataset.h5

phase:
	python3 tools/generate_phase_plot.py --entropy output/xi_entropy_log.npy --drift output/drift_tensor_Xi.npy

mpi:
	mpirun -n 4 python3 sim/parallel_launcher.py

clean:
	rm -f output/*.npy plots/*.png

stability:
	python3 tools/xi_chi_stability_analysis.py

report:
	python3 tools/generate_report.py

serve:
	gunicorn app:server --bind 0.0.0.0:8050 --workers 2
