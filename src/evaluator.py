import subprocess
import os

# Import our own neato files
from utils import * # for text file parsing
from plane_geometry import PlaneGeometry

avl_exe_path = os.join("lib", "avl", "avl3.35")
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

		self.plane_geometries = []

		self.generate_plane_geometries()
		self.generate_avl_files()
		self.generate_run_files()

	def generate_plane_geometries(self):
		# iterate through design points
		print("Generating Plane Geometries")
		for i in range(self.design_sweep_dict['num_design_points']):
			# load in all relevant dictionary entries for current design point
			design_point_dict = element_dict_from_lists_dict(self.design_sweep_dict, i)
			# created a dictionary of variables for a single design point
			print("========================================")
			print("===== Design Point # {} =====".format(i))
			print("{}".format(design_point_dict))
			print("===== Plane Geometry =====")
			self.plane_geometries.append(PlaneGeometry(design_point_dict, self.design_rules_filename))
		print("========================================")

	def generate_avl_files(self):
		# create output directory if it doesn't yet exist
		if not os.path.isdir(output_dirname):
			os.mkdir(output_dirname)
		# fill output directory with geometry .txt, .run, and .dat files
		for i in range(len(self.plane_geometries)):
			self.plane_geometries[i].generate_files(os.join(output_dirname, "plane_geom_{}".format(i)))

	def generate_run_files(self):
		for test_point_num in range(self.test_points_dict["num_test_points"]):
			# test point var lists are subscriptable
			for geom_num in range(len(self.plane_geometries)):
				test_point_dict = element_dict_from_lists_dict(self.test_points_dict, test_point_num)
				self.plane_geometries[geom_num].generate_run_file(
					os.join(output_dirname, "plane_geom_{}".format(geom_num)),
					os.join(output_dirname, "plane_geom_{}_test_point_{}".format(geom_num, test_point_num)),
					test_point_dict)

	def evaluate_plane_geometries(self):
		for geom_num in range(len(self.plane_geometries)):
			print("Evaluating Geometry #{}".format(geom_num))
			for test_point_num in range(self.test_points_dict["num_test_points"]):
				plane_geometry_filename_no_ext = os.join(output_dirname, "plane_geom_{}_test_point_{}".format(
					geom_num,
					test_point_num))
				# TODO: launch and run AVL with run file, interpret results
				print("OPEN FILE {}".format(plane_geometry_filename_no_ext))
				subprocess.call("{} < {}"
					.format(
						avl_exe_path,
						plane_geometry_filename_no_ext + ".run"),
					shell = True)

		print("EVAL PLANE GEOMSSSSES")