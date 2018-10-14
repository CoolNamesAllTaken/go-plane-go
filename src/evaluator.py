import subprocess

# Import our own neato files
from utils import * # for text file parsing
from plane_geometry import PlaneGeometry

avl_exe_path = "bin/avl3.35"
output_dirname = "output"

"""
Evaluates a set of design rules using a sweep of design points.
"""
class Evaluator:

	"""
	Constructor
	"""
	def __init__(self, design_rules_filename, design_sweep_filename):
		self.design_rules_filename = design_rules_filename
		self.design_sweep_dict = parse_text_file(design_sweep_filename)

		self.plane_geometries = []
		self.plane_geometry_filenames = []

		self.generate_plane_geometries()
		self.create_avl_files()

	def generate_plane_geometries(self):
		# iterate through design points
		print("Generating Plane Geometries")
		for i in range(self.design_sweep_dict['num_test_points']):
			design_point_dict = {}
			# load in all relevant dictionary entries for current design point
			for key in self.design_sweep_dict.keys():
				# design point var lists are subscriptable
				if not isinstance(self.design_sweep_dict[key], list):
					continue
				design_point_dict[key] = self.design_sweep_dict[key][i]
			# created a dictionary of variables for a single design point
			print("========================================")
			print("===== Design Point # {} =====".format(i))
			print("{}".format(design_point_dict))
			print("===== Plane Geometry =====")
			self.plane_geometries.append(PlaneGeometry(design_point_dict, self.design_rules_filename))
		print("========================================")

	def create_avl_files(self):
		# create output directory if it doesn't yet exist
		if not os.path.isdir(output_dirname):
			os.mkdir(output_dirname)
		# fill output directory with geometry .txt, .run, and .dat files
		for i in range(len(self.plane_geometries)):
			self.plane_geometries[i].generate_files(output_dirname + "/plane_geom_" + str(i))

	def evaluate_plane_geometries(self):
		for i in range(len(self.plane_geometries)):
			print("Evaluating Geometry #{}".format(i))
			plane_geometry_filename_no_ext = output_dirname + "/plane_geom_" + str(i)
			# TODO: launch and run AVL with run file, interpret results
			print("OPEN FILE {}".format(plane_geometry_filename_no_ext))
			


		print("EVAL PLANE GEOMSSSSES")