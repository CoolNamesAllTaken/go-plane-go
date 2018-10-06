from utils import *

class PlaneGeometry:

	# Constructor
	'''
	Inputs:
		config_filename = path to filename that defines basic aircraft parameters
	'''
	def __init__(self, config_filename, optimizer_vars):
		self.vars = optimizer_vars
		parse_text_file(config_filename, self.vars)
		print(self.vars)

	def calc_params(self):
		self.vars['wing_area'] = self.config_vars['rho'] * self.optimizer_vars['thrust_kg']

			
	# Calculate the mass of a rectangular prism
	def findMassPrism (length, width, height, density):
		vol = length * width * height
		mass = vol * density

	#Calculate the mass of a hollow tube
	def findMassTube (OD, ID, length, rho):
		vol = ( (OD/2)**2 * pi - (OD/2)**2 * pi ) * length
		mass = vol * rho

	#Calculate total mass of plane
	def calc_mass(self):
		#return self.vars["wing_chord"] * self.vars["wing_span"]

		#Mass of the wing
		totalMass = 0
		wing_thickness = self.vars['wing_chord'] * 0.12
		wing_rho = 0.02811738725 * 0.001 #g/mm^3
		wing_mass = findMassPrism(self.vars['wing_span'], self.vars['wing_chord'], wing_thickness, wing_rho)
		totalMass += wing_mass
		
		#Mass of the fuselage (2x)
		fuse_width = self.vars['fuse_diameter']
		fuse_height = self.vars['fuse_diameter']
		fuse_thickness = 0.48 * 10 #mm
		fuse_rho = 0.05920150729 * 0.001 #g/mm^3
		fuse_mass = findMassPrism(self.vars['fuse_length'], fuse_width, fuse_height, fuse_rho) - findMassPrism(self.vars['fuse_length'] - fuse_thickness, fuse_width - fuse_thickness, fuse_height - fuse_thickness, fuse_rho)
		totalMass += 2 * fuse_mass
		
		#Mass of the Vtail (2x)
		vtail_thickness = self.vars['vtail_chord'] * 0.12
		vtail_rho = wing_rho
		vtail_mass = findMassPrism(self.vars['vtail_span'], self.vars['vtail_chord'], vtail_thickness, vtail_rho)
		totalMass += 2 * vtail_mass
		
		#Mass of the Htail
		htail_thickness = self.vars['htail_chord'] * 0.12
		htail_rho = wing_rho
		htail_mass = findMassPrism(self.vars['htail_chord'], self.vars['htail_span'], htail_thickness, htail_rho)
		totalMass += htail_mass
		
		#Mass of the tail booms (2x)
		tail_boom_OD = 0.8 * 10 * 2 #mm
		tail_boom_ID = 0.7 * 10 * 2 #mm
		tail_boom_len = self.vars['vtail_distance'] + self.vars['vtail_chord']
		tail_boom_rho = 1.549108113 * 0.001 #g/mm^3
		tail_boom_mass = findMassTube(tail_boom_OD, tail_boom_ID, tail_boom_len, tail_boom_rho)
		totalMass += 2 * tail_boom_mass
		
		#Mass of the wing spar
		wing_spar_Owidth = 1 * 10 # mm
		wing_spar_Iwidth = 0.85 * 10 #mm
		wing_spar_Oheight = wing_spar_Owidth
		wing_spar_Iheight = wing_spar_Iwidth
		wing_spar_length = self.vars['wing_span']
		wing_spar_rho = 1.54954955 * 0.001 #g/mm^3
		wing_spar_mass = findMassPrism(wing_spar_Owidth, wing_spar_Oheight, wing_spar_length, wing_spar_rho) - findMassPrism(wing_spar_Iwidth, wing_spar_Iheight, wing_spar_length, wing_spar_rho)
		totalMass += wing_spar_mass

		print(totalMass)

		return totalMass




