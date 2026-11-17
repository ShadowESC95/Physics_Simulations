import subprocess
import os

class GadgetRunner:
    def __init__(self, executable="./Gadget2", param_file="galaxy.param"):
        self.executable = executable
        self.param_file = param_file

    def run(self):
        if not os.path.exists(self.executable):
            raise RuntimeError("Gadget binary not found.")
        cmd = [self.executable, self.param_file]
        return subprocess.run(cmd).returncode == 0
