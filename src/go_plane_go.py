import numpy as np 
import matplotlib.pyplot as plt
import os.path

# for testing only
from utils import *

from evaluator import Evaluator

# NOTE: this program MUST be run from the go-plane-go directory

design_rules_filename = os.path.join("config","twin_boom_v1.txt")
design_sweep_filename = os.path.join("config","design_sweep.txt")
test_points_filename = os.path.join("config","test_points.txt")

def main():
	generate_plane_geometries()
	# our_plane = PlaneGeometry("config/test_parser.txt")

def generate_plane_geometries():
	eval = Evaluator(design_rules_filename, design_sweep_filename, test_points_filename)
	eval.evaluate_plane_geometries()
if __name__ == "__main__":
	main()