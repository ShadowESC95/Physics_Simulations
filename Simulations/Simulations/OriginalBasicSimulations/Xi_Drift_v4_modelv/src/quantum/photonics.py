# src/quantum/photonic.py
import strawberryfields as sf
from strawberryfields.ops import *

prog = sf.Program(4)
with prog.context as q:
    Fock(2) | q[0]
    BSgate(0.5, 0.1) | (q[0], q[1])
    MeasureFock() | q
