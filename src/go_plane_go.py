import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # for 3d plotting
import os.path
import argparse

from evaluator import Evaluator

from utils import *

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


	# mission 1 analysis
	# run AVL and reuse results for m2, m3
	m1_results_list = eval.evaluate_plane_geometries(run_avl=not args.plotonly, 
		post_process_filename="config/post_process/mission_1_post_process.txt")
	calculate_cruise_conditions(m1_results_list)
	m1_score = np.ones(len(m1_results_list))
	
	print("===M1 SCORE===")
	print(m1_score)

	# mission 2 analysis
	m2_results_list = eval.evaluate_plane_geometries(run_avl=False,
		post_process_filename="config/post_process/mission_2_post_process.txt")
	calculate_cruise_conditions(m2_results_list)
	# lap time for each geometry
	m2_lap_time_list = np.asarray([m2_result["time_lap"] for m2_result in m2_results_list])
	m2_time_list = 3.0 *  m2_lap_time_list + 90.0 # assume 30sec / turn
	# min lap time of all teams for m2
	m2_time_min_list = np.asarray([m2_result["time_min"][0] for m2_result in m2_results_list])
	m2_score = 1.0 + (m2_time_min_list / m2_time_list) # scores for each geometry
	
	print("===M2 SCORE===")
	print(m2_score)


	# mission 3 analysis
	m3_results_list = eval.evaluate_plane_geometries(run_avl=False,
		post_process_filename="config/post_process/mission_3_post_process.txt")
	calculate_cruise_conditions(m3_results_list)
	m3_endurance_list = np.asarray([m3_result["endurance"][0] * 60 for m3_result in m3_results_list]) # seconds
	m3_time_lap_list = np.asarray([m3_result["time_lap"] for m3_result in m3_results_list])
	m3_laps = np.floor(m3_endurance_list / m3_time_lap_list)
	m3_score = 2.0 + m3_laps
	
	print("===M3 SCORE===")
	print(m3_score)

	# total score
	total_score = m1_score + m2_score + m3_score

	# score histogram
	fig = plt.figure("Scores")
	ax = fig.add_subplot(111)
	bar_locations = np.arange(len(m3_score))
	bar_width = 0.2
	ax.bar(bar_locations - 2*bar_width, m1_score, width=bar_width, label="M1 Score")
	ax.bar(bar_locations - bar_width, m2_score, width=bar_width, label="M2 Score")
	ax.bar(bar_locations, m3_score, width=bar_width, label="M3 Score")
	ax.bar(bar_locations + bar_width, total_score, width=bar_width, label="Total Score")
	plt.xticks(bar_locations)
	plt.xlabel("Geometry Number")
	plt.ylabel("Total Score")
	plt.title("Total Scores for Tested Geometries")
	plt.grid()
	plt.legend()

	# D, T vs. v plot
	plot_result_vars_vs_tp(m1_results_list, "v", "T")
	for i in range(len(m1_results_list)):
		plt.plot(m1_results_list[i]["v"], m1_results_list[i]["D"], "--")
	plt.xlabel("Velocity (m/s)")
	plt.ylabel("Drag (Dashed), Thrust (Solid) (N)")
	plt.title("Drag and Thrust vs. Velocity")
	plot_result_vars_vs_tp(m1_results_list, "CDtot", "CLtot")
	plot_result_vars_vs_geom(m2_results_list, "time_lap")
	plot_result_vars_vs_geom(m2_results_list, "v")
	
	# plot 3D contour of designs in t/w ratio : endurance space
	thrust_static = np.asarray(slice_list_of_dicts(m1_results_list, "thrust_static")) * 9.81 # in N
	plane_weight = np.asarray(slice_list_of_dicts(m1_results_list, "plane_weight"))
	tw_ratio = thrust_static / plane_weight
	endurance = np.asarray(slice_list_of_dicts(m1_results_list, "endurance"))
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_trisurf(
		tw_ratio, 
		endurance,
		total_score,
		shade=True)
	ax.set_xlabel("Thrust to Weight Ratio")
	ax.set_ylabel("Endurance (minutes)")
	ax.set_zlabel("Total Score")
	ax.set_title("Design Scores in the Thrust to Weight Ratio vs. Endurance Space")

	# plot 3D contour of designs in v_cruise: endurance space
	v_cruise = np.asarray(slice_list_of_dicts(m1_results_list, "v_cruise"))
	endurance = np.asarray(slice_list_of_dicts(m1_results_list, "endurance"))
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_trisurf(
		v_cruise, 
		endurance,
		total_score,
		shade=True)
	ax.set_xlabel("Cruise Velocity (m/s)")
	ax.set_ylabel("Endurance (minutes)")
	ax.set_zlabel("Total Score")
	ax.set_title("Design Scores in the Cruise Velocity vs. Endurance Space")

	plt.show()

def calculate_cruise_conditions(results_list):
	# iterate through plane geometries
	for i in range(len(results_list)):
		# list dictionary with results for a test point
		results_list[i]["v"] = np.sqrt((results_list[i]["plane_weight"] / 
			(0.5 * results_list[i]["rho"] * results_list[i]["Sref"] * results_list[i]["CLtot"])))
		# linear interpolation of thrust
		results_list[i]["thrust"] = (results_list[i]["v_pitch"] - results_list[i]["v"]) / results_list[i]["v_pitch"] * results_list[i]["thrust_static"]
		results_list[i]["q_inf"] = 0.5 * results_list[i]["rho"] * results_list[i]["v"]**2 
		results_list[i]["T"] = results_list[i]["thrust"] * 9.81 # convert to Newtons from kg
		results_list[i]["L"] = results_list[i]["q_inf"] * results_list[i]["Sref"] * np.asarray(results_list[i]["CLtot"])
		results_list[i]["D"] = results_list[i]["q_inf"] * results_list[i]["Sref"] * results_list[i]["CDtot"]

		# find thrust where T = D
		thrust_excess = results_list[i]["T"] - results_list[i]["D"]
		results_list[i]["v_cruise"] = np.interp(0, thrust_excess, results_list[i]["v"]) # m/s
		results_list[i]["time_lap"] = 610.0 / results_list[i]["v_cruise"] + 30 # seconds

def plot_results(results_list):
	plot_result_vars_vs_tp(results_list, "Alpha", "CLtot")
	plot_result_vars_vs_tp(results_list, "Alpha", "CDtot")
	plt.show()

"""
Plots var_2_name (y) vs. var_1_name (x) for each geometry across test points
"""
def plot_result_vars_vs_tp(results_list, var_1_name, var_2_name, new_figure=True):
	if new_figure:
		plt.figure("{} vs. {}".format(var_2_name, var_1_name))
		plt.title("{} vs. {}".format(var_2_name, var_1_name))
	for i in range(len(results_list)):
		plt.plot(results_list[i][var_1_name], results_list[i][var_2_name], label="Plane Geometry {}".format(i))
	plt.xlabel(var_1_name)
	plt.ylabel(var_2_name)
	plt.grid()
	plt.legend()

"""
Plots var_name (y) across geometries.  If var is subscriptable, takes the first entry.
"""
def plot_result_vars_vs_geom(results_list, var_name, new_figure=True):
	if new_figure:
		plt.figure("{} vs. Geom".format(var_name))

	var_list = slice_list_of_dicts(results_list, var_name)
	
	geom_list = range(len(results_list))
	plt.plot(geom_list, var_list, label=var_name)
	plt.xlabel("Geometry")
	plt.ylabel(var_name)
	plt.grid()
	plt.legend()
	
if __name__ == "__main__":
	main()