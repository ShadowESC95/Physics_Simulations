# src/neuromorphic/lava_processor.py
from lava.proc import LIF, Dense

network = Network()
lif1 = LIF(shape=(128, 128))
dense = Dense(weights=load_xi_weights())
network.add_process(lif1, "XiProcessor")
