from pennylane import device

def get_qdevice(name: str):
    if name == "ibmq":
        return device("qiskit.ibmq", wires=4, backend="ibmq_qasm_simulator")
    elif name == "rigetti":
        return device("forest.qvm", device="4q-qvm")
    return device("default.qubit", wires=4)
