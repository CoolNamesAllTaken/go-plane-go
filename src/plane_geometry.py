from utils import *

import os.path # for filename extension stripping
import numpy as np

avl_airfoil_dirname = "avl/airfoils/"

class PlaneGeometry:
	"""
	Constructor
	Inputs:
		design_point_dict 		= 	dictionary of variables that will be used with the design rules to
									construct the aircraft
		design_rules_filename 	= 	path to .txt file where rules that will be used to evaluate the design point are stored
	Returns:
		PlaneGeometry object
	"""
	def __init__(self, design_point_dict, design_rules_filename):
		self.vars = design_point_dict # initialize design point
		parse_text_file(design_rules_filename, self.vars) # evaluate design rules at design point
		print(self.vars)

	"""
	Outputs the PlaneGeometry as an AVL-readable text file
	Inputs:
		filename_no_ext = path to output file without extension (will be created if it doesn't exist)
	"""
	def generate_files(self, filename_no_ext):
		self.generate_avl_file(filename_no_ext)

	"""
	Generates a .run file named filename_no_ext.run that will run this geometry with the parameters in test_point_dict
	Inputs:
		avl_filename_no_ext = name of associated .avl file
		run_filename_no_ext = name of the .run file to be created
		test_point_dict = dictionary of the relevant test conditions
	"""
	def generate_run_file(self, avl_filename_no_ext, run_filename_no_ext, test_point_dict):
		with open(run_filename_no_ext + ".run", "w+") as f:
			f.write("LOAD {}\n".format(avl_filename_no_ext + ".avl"))
			f.write("OPER\n")
			f.write("c1\n")
			f.write("M {:.3f}\n".format(self.vars["rho"]))
			f.write("D {:.3f}\n".format(self.vars["rho"]))
			f.write("G 9.81\n")
			f.write("X {:.3f}\n\n".format(self.vars["wing_chord"]/4))
			f.write("D1 D1 {:.3f}\n".format(self.vars["flap_TO"]))
			f.write("D3 PM 0\n")
			f.write("A A {}\n".format(test_point_dict["alpha"]))
			f.write("X\n")
			f.write("ST\n")
			f.write("{}\n".format(run_filename_no_ext + "_trim.txt")) # TODO: generate trim file
			f.write("O\n\n\n")
			f.write("Quit\n")
		
	"""
	Generates an .avl file containing the aircraft geometry
	Inputs:
		filename_no_ext = path to output file without extension (will be created if it doesn't exist)
	"""
	def generate_avl_file(self, filename_no_ext):
		# overwrite file or create file if it doesn't exist
		with open(filename_no_ext + ".avl", "w+") as f:
			## Configuration Stuff
			f.write("{}\n".format(self.vars["name"])) # name of aircraft
			f.write("{}\n\n".format(self.vars["mach"])) # mach number
			f.write("#IYsym     IZsym     IZsym\n") # symmetry line
			f.write("0         0         0\n\n") # reference area
			f.write("#Sref     Cref         Bref\n")
			f.write("{:.3f}     {:.3f}     {:.3f}\n\n".format(
				self.vars["wing_area"],
				self.vars["wing_chord"],
				self.vars["wing_span"]))
			# reference point, overwritten later by CG definition
			f.write("#Xref     Yref         Zref\n")
			f.write("0         0         0\n\n")
			# profile drag estimate
			f.write("#Profile Drag\n")
			f.write("0.06\n\n")

			## Fuselage
			# create fuselage.dat file
			fuse_filename = filename_no_ext + "_fuse.dat"
			self.generate_fuse_file(fuse_filename)
			# more than one fuselage: use twin fuselage config
			if self.vars["fuse_y"] > 0:
				# left fuselage
				f.write("#==============================================\n") # section break
				f.write("BODY\nFuselage Left\n\n") # declare left fuselage
				f.write("#NLengthwise     Spacing\n") # source distribution
				f.write("{}            3\n\n".format(np.ceil(self.vars["fuse_length"]/0.01)))
				f.write("TRANSLATE\n0.0     {:.3f}    0.0\n\n".format(-self.vars["fuse_y"]))
				f.write("BFIL\n{}\n\n".format(fuse_filename)) # fuselage file at no_ext_filename.dat

				# right fuselage
				f.write("#==============================================\n") # section break
				f.write("BODY\nFuselage Right\n\n") # declare left fuselage
				f.write("#NLengthwise     Spacing\n") # source distribution
				f.write("{}            3\n\n".format(np.ceil(self.vars["fuse_length"]/0.01)))
				f.write("TRANSLATE\n0.0     {:.3f}    0.0\n\n".format(-self.vars["fuse_y"]))
				f.write("BFIL\n{}\n\n".format(fuse_filename)) # fuselage file at no_ext_filename.dat
			# single fuselage
			else:
				f.write("#==============================================\n") # section break
				f.write("BODY\nFuselage\n\n") # declare left fuselage
				f.write("#NLengthwise     Spacing\n") # source distribution
				f.write("{}            3\n\n".format(np.ceil(self.vars["fuse_length"]/0.01)))
				f.write("TRANSLATE\n0.0     {:.3f}    0.0\n\n".format(-self.vars["fuse_y"]))
				f.write("BFIL\n{}\n\n".format(fuse_filename)) # fuselage file at no_ext_filename.dat

			f.write("#==============================================\n") # section break
			f.write("SURFACE\nInboard Wing\n\n") #declare inboard wing
			f.write("#NChordwise    Spacing\n") #source distribution
			f.write("10            3\n\n")
			f.write("ANGLE\n{:.1f}\n\n".format(self.vars["wing_incidence"])) #declare wing incidence
			f.write("YDUPLICATE\n0.0\n\n")
			f.write("SCALE\n1.0    1.0    1.0\n\n") #scaling
			f.write("TRANSLATE\n0.0   0.0   0.0\n\n") #translation
			f.write("#----------------------------------------------\n") #Surface section break
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("0   0   {:.2f}   {:.2f}   0   {}   3\n\n".format(
				self.vars["fuse_diameter"]/2,
				self.vars["wing_chord"],
				np.ceil(self.vars["fuse_y"]/0.02)))
			f.write("NACA\n0012\n\n") #airfoil
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Flap definition
			f.write("flap        1.0        0.7            0. 0. 0.        1.0\n\n") 
			
			f.write("#----------------------------------------------\n") #Surface section break
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("0   {:.1f}   {:.2f}   {:.2f}   0   {}   3\n\n".format(
				self.vars["fuse_y"], self.vars["fuse_diameter"]/2,
				self.vars["wing_chord"],
				np.ceil(self.vars["fuse_y"]/0.02)))
			f.write("NACA\n0012\n\n") #airfoil
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Flap definition
			f.write("flap        1.0        0.7            0. 0. 0.        1.0\n\n") 
			
			f.write("#==============================================\n") # section break
			f.write("SURFACE\nOutboard Wing\n\n") #declare outboard wing
			f.write("#NChordwise    Spacing\n") #source distribution
			f.write("10            3\n\n")
			f.write("ANGLE\n{:.1f}\n\n".format(self.vars["wing_incidence"])) #declare wing incidence
			f.write("YDUPLICATE\n0.0\n\n")
			f.write("SCALE\n1.0    1.0    1.0\n\n") #scaling
			f.write("TRANSLATE\n0.0   0.0   0.0\n\n") #translation
			
			f.write("#----------------------------------------------\n") #Surface section break
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("0   {:.1f}   {:.2f}   {:.2f}   0   {}   3\n\n".format(
				self.vars["fuse_y"], self.vars["fuse_diameter"]/2,
				self.vars["wing_chord"],
				np.ceil(self.vars["fuse_y"]/0.02)))
			f.write("AFIL 0.0 1.0\n") #Airfoil
			f.write(avl_airfoil_dirname + "{:s}\n\n".format(self.vars["wing_airfoil"]))
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Flap definition
			f.write("flap        1.0        0.7            0. 0. 0.        1.0\n\n") 
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Aileron definition
			f.write("aileron        1.0        0.7            0. 0. 0.        -1.0\n\n") 
			
			f.write("#----------------------------------------------\n") #Surface section break
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("0   {:.1f}   {:.2f}   {:.2f}   0\n\n".format(
				self.vars["wing_span"]/2,
				self.vars["fuse_diameter"]/2,
				self.vars["wing_chord"]))
			f.write("AFIL 0.0 1.0\n") #Airfoil
			f.write(avl_airfoil_dirname + "{:s}\n\n".format(self.vars["wing_airfoil"]))
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Flap definition
			f.write("flap        1.0        0.7            0. 0. 0.        1.0\n\n") 
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Aileron definition
			f.write("aileron        1.0        0.7            0. 0. 0.        -1.0\n\n") 
			
			f.write("#==============================================\n") # section break
			f.write("SURFACE\nHStab\n\n") #declare Hstab
			f.write("#NChordwise    Spacing\n") #source distribution
			f.write("10            3\n\n")
			f.write("ANGLE\n{:.1f}\n\n".format(self.vars["stab_incidence"])) #declare stab incidence
			f.write("YDUPLICATE\n0.0\n\n")
			f.write("SCALE\n1.0    1.0    1.0\n\n") #scaling
			f.write("TRANSLATE\n0.0   0.0   0.0\n\n") #translation
			
			f.write("#----------------------------------------------\n") #Surface section break
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("{:.3f}   0   {:.2f}   {:.2f}   0   {}   3\n\n".format(
				self.vars["htail_distance"], self.vars["fuse_diameter"]+self.vars["vtail_span"],
				self.vars["htail_chord"],
				np.ceil(self.vars["fuse_y"]/0.02)))
			f.write("NACA\n0012\n\n") #Airfoil
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Elevator definition
			f.write("elevator        1.0        0.7            0. 0. 0.        1.0\n\n")
			
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("{:.3f}   {:.3f}   {:.2f}   {:.2f}   0   {}   3\n\n".format(
				self.vars["htail_distance"],
				self.vars["htail_span"]/2,
				self.vars["fuse_diameter"]+self.vars["vtail_span"],
				self.vars["htail_chord"],
				np.ceil(self.vars["fuse_y"]/0.02)))
			f.write("NACA\n0012\n\n") #Airfoil
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Elevator definition
			f.write("elevator        1.0        0.7            0. 0. 0.        1.0\n\n")

			f.write("#==============================================\n") # section break
			f.write("SURFACE\nVstab Left\n\n") #declare Fin
			f.write("#NChordwise    Spacing\n") #source distribution
			f.write("10            3\n\n")
			f.write("ANGLE\n0\n\n") #declare fin incidence
			f.write("SCALE\n1.0    1.0    1.0\n\n") #scaling
			f.write("TRANSLATE\n0.0   0.0   0.0\n\n") #translation
			f.write("#----------------------------------------------\n") #Surface section break
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("{:.3f}   {:.3f}   {:.2f}   {:.2f}   0   {}   3\n\n".format(
				self.vars["vtail_distance"],
				-self.vars["fuse_y"],
				self.vars["fuse_diameter"],
				self.vars["vtail_chord"],
				np.ceil(self.vars["vtail_span"]/0.02)))
			f.write("NACA\n0012\n\n") #Airfoil
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Rudder definition
			f.write("rudder        1.0        0.7            0. 0. 0.        1.0\n\n") 
			
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("{:.3f}   {:.3f}   {:.2f}   {:.2f}   0   {}   3\n\n".format(
				self.vars["vtail_distance"],
				-self.vars["fuse_y"],
				self.vars["fuse_diameter"]+self.vars["vtail_span"],
				self.vars["vtail_chord"],
				np.ceil(self.vars["vtail_span"]/0.02)))
			f.write("NACA\n0012\n\n") #Airfoil
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Rudder definition
			f.write("rudder        1.0        0.7            0. 0. 0.        1.0\n\n")            
			f.write("#==============================================\n") # section break
			f.write("SURFACE\nVstab Right\n\n") #declare Fin
			f.write("#NChordwise    Spacing\n") #source distribution
			f.write("10            3\n\n")
			f.write("ANGLE\n0\n\n") #declare fin incidence
			f.write("SCALE\n1.0    1.0    1.0\n\n") #scaling
			f.write("TRANSLATE\n0.0   0.0   0.0\n\n") #translation
			f.write("#----------------------------------------------\n") #Surface section break
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("{:.3f}   {:.3f}   {:.2f}   {:.2f}   0   {}   3\n\n".format(
				self.vars["vtail_distance"],
				self.vars["fuse_y"],
				self.vars["fuse_diameter"],
				self.vars["vtail_chord"],
				np.ceil(self.vars["vtail_span"]/0.02)))
			f.write("NACA\n0012\n\n") #Airfoil
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Rudder definition
			f.write("rudder        1.0        0.7            0. 0. 0.        1.0\n\n") 
			
			f.write("SECTION\n")
			f.write("#XLE   YLE   ZLE   Chord   Incidence   Nspan   Spacing\n") #Section geometry
			f.write("{:.3f}   {:.3f}   {:.2f}   {:.2f}   0   {}   3\n\n".format(
				self.vars["vtail_distance"],
				self.vars["fuse_y"],
				self.vars["fuse_diameter"]+self.vars["vtail_span"],
				self.vars["vtail_chord"],
				np.ceil(self.vars["vtail_span"]/0.02)))
			f.write("NACA\n0012\n\n") #Airfoil
			f.write("CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n") #Rudder definition
			f.write("rudder        1.0        0.7            0. 0. 0.        1.0\n\n")

	"""
	Creates a data file with coordinates defining the aircraft's fuselage
	Inputs:
		fuse_filename = file path to store coordinates in (should be .dat)
	"""
	def generate_fuse_file(self, fuse_filename):
		# create array of x coordinates from nose->tail->nose
		fuse_x_arr = np.arange(
			0,
			self.vars["fuse_diameter"]/2,
			step = self.vars["fuse_diameter"]/20)
		fuse_x_arr = np.append(fuse_x_arr,
			np.arange(
				self.vars["fuse_diameter"]/2+(self.vars["fuse_diameter"])/10,
				self.vars["fuse_length"] - self.vars["fuse_diameter"]/2,
				step = self.vars["fuse_diameter"]/10))
		fuse_x_arr = np.append(fuse_x_arr,
			np.arange(
				self.vars["fuse_length"] - self.vars["fuse_diameter"]/2 + self.vars["fuse_diameter"]/20,
				self.vars["fuse_length"],
				step = self.vars["fuse_diameter"]/20))
		fuse_x_arr = np.append(fuse_x_arr, np.flipud(fuse_x_arr)[1:-1]) # append reversed array to end, without overlapping the last point

		# write coordinates to .dat file
		with open(fuse_filename, "w+") as f:
			for i in range(len(fuse_x_arr)):
				# nose
				if (fuse_x_arr[i] < self.vars["fuse_diameter"]/2):
					delta = np.sqrt(-(-fuse_x_arr[i] + self.vars["fuse_diameter"]/2)**2 + (self.vars["fuse_diameter"]/2)**2)
				# body
				elif (fuse_x_arr[i] < self.vars["fuse_length"] - self.vars["fuse_diameter"]/2):
					delta = self.vars["fuse_diameter"]/2
				# tail
				else:
					delta = np.sqrt(-(fuse_x_arr[i] - (self.vars["fuse_length"] - self.vars["fuse_diameter"]/2))**2 + self.vars["fuse_diameter"]**2)

				# starboard side
				if i < len(fuse_x_arr)/2:
					f.write("{:.3f}        {:.4f}\n".format(self.vars["fuse_x"] + fuse_x_arr[i], self.vars["fuse_z"] + delta))
				# port side
				else:
					f.write("{:.3f}        {:.4f}\n".format(self.vars["fuse_x"] + fuse_x_arr[i], self.vars["fuse_z"] - delta))
