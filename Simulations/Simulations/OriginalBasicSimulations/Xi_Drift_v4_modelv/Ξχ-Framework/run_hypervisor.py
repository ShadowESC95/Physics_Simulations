import argparse
from hypervisor.display_core import QuantumDisplay

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--layout", default="default")
    parser.add_argument("--data-sources", nargs='+')
    parser.add_argument("--compute-backend", choices=['quantum', 'hpc'], default='hpc')
    args = parser.parse_args()
    
    display = QuantumDisplay(layout=args.layout)
    display.run()
