import subprocess
import os.path

# Import our own neato files
from utils import * # for text file parsing
from plane_geometry import PlaneGeometry

avl_exe_path = os.path.join("lib", "avl", "avl3.35")
output_dirname = "output"

"""
Evaluates a set of design rules using a sweep of design points.
"""
class Evaluator:

	"""
	Constructor
	Inputs:
		design_rules_filename = .txt file of design rules used to evaluate each point in the design sweep
		design_sweep_filename = .txt file containing sweep of relevant design parameters to generate geometries for
		test_points_filename = .txt file containing relevant test data for test points (AoA, etc)
	"""
	def __init__(self, design_rules_filename, design_sweep_filename, test_points_filename):
		self.design_rules_filename = design_rules_filename
		self.design_sweep_dict = parse_text_file(design_sweep_filename)
		self.test_points_dict = parse_text_file(test_points_filename)

		# initialize by creating aircraft geometries and necessary files for running avl test points
		self.plane_geometries = []
		self.generate_plane_geometries()
		self.generate_avl_files()
		self.generate_run_files()

	"""
	Generates one aircraft geometry object for each design point (design point = design rules evaluated at a point on the design sweep).
	"""
	def generate_plane_geometries(self):
		# iterate through design points
		print("Generating Plane Geometries")
		for i in range(self.design_sweep_dict['num_design_points']):
			# load in all relevant dictionary entries for current design point
			design_point_dict = element_dict_from_list_dict(self.design_sweep_dict, i)
			# created a dictionary of variables for a single design point
			print("========================================")
			print("===== Design Point # {} =====".format(i))
			print("{}".format(design_point_dict))
			print("===== Plane Geometry =====")
			self.plane_geometries.append(PlaneGeometry(design_point_dict, self.design_rules_filename))
		print("========================================")

	"""
	Generates the files that AVL uses to construct an aircraft.
	"""
	def generate_avl_files(self):
		# create output directory if it doesn't yet exist
		if not os.path.isdir(output_dirname):
			os.mkdir(output_dirname)
		# fill output directory with geometry .txt, .run, and .dat files
		for i in range(len(self.plane_geometries)):
			self.plane_geometries[i].generate_files(os.path.join(output_dirname, "plane_geom_{}".format(i)))

	"""
	Generates the files that AVL uses to set up the simulation for an aircraft.
	"""
	def generate_run_files(self):
		for test_point_num in range(self.test_points_dict["num_test_points"]):
			# test point var lists are subscriptable
			for geom_num in range(len(self.plane_geometries)):
				test_point_dict = element_dict_from_list_dict(self.test_points_dict, test_point_num)
				self.plane_geometries[geom_num].generate_run_file(
					os.path.join(output_dirname, "plane_geom_{}".format(geom_num)),
					os.path.join(output_dirname, "plane_geom_{}_test_point_{}".format(geom_num, test_point_num)),
					test_point_dict)

	"""
	Runs the geometries through AVL for all test points and returns the result.
	Output:
		results_list = list of list dictionaries, where each dictionary containst the results for a single geometry across all its
						test points (results_list[0]['Alpha'] returns a list of alpha values for geometry 0 across all test points)
		run_avl = disables data analysis when set to False (good for just plotting stuff)
	"""
	def evaluate_plane_geometries(self, run_avl=True):
		# list of list dictionaries, where each dictionary contains the results for a single geometry across all its test points
		results_list = [] # results_list[0]['Alpha'] returns a list of alpha values for geometry 0 across all test points
		# evaluate each aircraft geometry
		for geom_num in range(len(self.plane_geometries)):
			print("Evaluating Geometry #{}".format(geom_num))
			# evaluate geometry at multiple test points
			test_point_results = []
			for test_point_num in range(self.test_points_dict["num_test_points"]):
				test_point_filename_no_ext = os.path.join(output_dirname, "plane_geom_{}_test_point_{}".format(
					geom_num,
					test_point_num))
				if run_avl:
					subprocess.call("{} < {}.run"
						.format(
							avl_exe_path,
							test_point_filename_no_ext),
						shell = True)
				test_point_results.append(parse_results_file("{}_trim.txt".format(test_point_filename_no_ext )))
				# print(test_point_results[test_point_num])
			# list dictionary of results for this plane geometry across all test points
			results_list.append(list_dict_from_element_dicts(test_point_results))
			# print(results_list[geom_num])
		return results_list

