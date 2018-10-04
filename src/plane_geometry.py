from utils import *

class PlaneGeometry:

	# Constructor
	'''

	'''
	def __init__(self, config_filename, optimizer_vars):
		self.vars = optimizer_vars
		parse_text_file(config_filename, self.vars)
		print(self.vars)

	def calc_params(self):
		self.vars['wing_area'] = self.config_vars['rho'] * self.optimizer_vars['thrust_kg']

