import numpy as np 
import matplotlib.pyplot as plt
import os.path
import argparse

from evaluator import Evaluator

# NOTE: this program MUST be run from the go-plane-go directory

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--plotonly", help="just plot stuff", action="store_true")
args = parser.parse_args()

design_rules_filename = os.path.join("config","design_rules","twin_boom_v1.txt")
design_sweep_filename = os.path.join("config","design_sweep","design_sweep.txt")
test_points_filename = os.path.join("config","test_points","test_points.txt")

def main():
	generate_plane_geometries()

def generate_plane_geometries():
	eval = Evaluator(design_rules_filename, design_sweep_filename, test_points_filename)
	if args.plotonly:
		results_list = eval.evaluate_plane_geometries(run_avl=False)
	else:
		results_list = eval.evaluate_plane_geometries(run_avl=True)
	plot_results(results_list)

def plot_results(results_list):
	plot_result_vars(results_list, "Alpha", "CLtot")
	plot_result_vars(results_list, "Alpha", "CDtot")
	plt.show()

"""
Plots var_2_name (y) vs. var_1_name (x)
"""
def plot_result_vars(results_list, var_1_name, var_2_name):
	plt.figure("{} vs. {}".format(var_2_name, var_1_name))
	for i in range(len(results_list)):
		plt.plot(results_list[i][var_1_name], results_list[i][var_2_name], label="Plane Geometry {}".format(i))
	plt.xlabel(var_1_name)
	plt.ylabel(var_2_name)
	plt.legend()
	
if __name__ == "__main__":
	main()