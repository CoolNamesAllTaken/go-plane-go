import numpy as np 
import matplotlib.pyplot as plt
import os.path
import argparse

from evaluator import Evaluator

# NOTE: this program MUST be run from the go-plane-go directory

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--plotonly", help="just plot stuff", action="store_true")
args = parser.parse_args()

design_rules_filename = os.path.join("config","twin_boom_v1.txt")
design_sweep_filename = os.path.join("config","design_sweep.txt")
test_points_filename = os.path.join("config","test_points.txt")

def main():
	generate_plane_geometries()
	# our_plane = PlaneGeometry("config/test_parser.txt")

def generate_plane_geometries():
	eval = Evaluator(design_rules_filename, design_sweep_filename, test_points_filename)
	if args.plotonly:
		results_list = eval.evaluate_plane_geometries(run_avl=False)
	else:
		results_list = eval.evaluate_plane_geometries(run_avl=True)
	plot_results(results_list)

def plot_results(results_list):
	for i in range(len(results_list)):
		plt.plot(results_list[i]["Alpha"], results_list[i]["CLtot"])
	plt.xlabel("Alpha")
	plt.ylabel("CLtot")
	plt.show()
if __name__ == "__main__":
	main()