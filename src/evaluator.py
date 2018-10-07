from utils import *

# Import our own neato files
from plane_geometry import PlaneGeometry

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
		for i in range(len(self.plane_geometries)):
			self.plane_geometries[i].print_to_file("output/plane_geom_" + str(i) + ".avl")

	def generate_plane_geometries(self):
		for i in range(self.design_sweep_dict['num_test_points']):
			design_point_dict = {}
			for key in self.design_sweep_dict.keys():
				# design point var lists are subscriptable
				if not isinstance(self.design_sweep_dict[key], list):
					continue
				design_point_dict[key] = self.design_sweep_dict[key][i]
			# created a dictionary of variables for a single design point
			print("DESIGN POINT: {}".format(design_point_dict))
			self.plane_geometries.append(PlaneGeometry(design_point_dict, self.design_rules_filename))
			

	def evaluate_plane_geometries(self):
		for i in range(len(plane_geometries)):
			print("Evaluating Geometry #{}".format(i))
			
		print("EVAL PLANE GEOMSSSSES")