
# Dockerfile for GPU-accelerated Ξ–χ scalar field simulation
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

RUN apt-get update && apt-get install -y python3-pip && \
    pip install matplotlib ipykernel notebook

WORKDIR /workspace
COPY xi_chi_simulation.ipynb /workspace/

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser"]
