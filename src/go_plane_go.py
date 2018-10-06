import numpy as np 
import matplotlib.pyplot as plt 

# for testing only
from utils import *

from evaluator import Evaluator

# NOTE: this program MUST be run from the go-plane-go directory

design_rules_filename = "config/twin_boom_v1.txt"
design_sweep_filename = "config/design_sweep.txt"

def main():
	generate_plane_geometries()
	# our_plane = PlaneGeometry("config/test_parser.txt")

def generate_plane_geometries():
	eval = Evaluator(design_rules_filename, design_sweep_filename)
	eval.generate_plane_geometries()

if __name__ == "__main__":
	main()