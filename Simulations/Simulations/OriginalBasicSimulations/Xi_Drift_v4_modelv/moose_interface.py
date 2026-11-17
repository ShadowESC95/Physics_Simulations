import subprocess
import os

class MOOSEBridge:
    def __init__(self, input_file="moose_simulation.i", binary_path="~/moose/modules/heat_conduction-opt"):
        self.input_file = input_file
        self.binary_path = os.path.expanduser(binary_path)

    def run(self):
        if not os.path.isfile(self.binary_path):
            raise FileNotFoundError("MOOSE binary not found.")
        cmd = [self.binary_path, "-i", self.input_file]
        result = subprocess.run(cmd, capture_output=True)
        print(result.stdout.decode())
        return result.returncode == 0
