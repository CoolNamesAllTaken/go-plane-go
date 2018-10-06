from utils import *

import os.path # for filename extension stripping
import numpy as np

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
		filename = path to output .txt file (will be created if it doesn't exist)
	"""
	def print_to_file(self, filename):
		# overwrite file or create file if it doesn't exist
		with open(filename, "w+") as f:
			## Configuration Stuff
			f.write("{}\n".format(self.vars["name"])) # name of aircraft
			f.write("{}\n\n".format(self.vars["mach"])) # mach number
			f.write("#IYsym     IZsym     IZsym\n") # symmetry line
			f.write("0         0         0\n\n") # reference area
			f.write("{:.3f}     {:.3f}     {:.3f}\n\n".format(self.vars["wing_area"], self.vars["wing_chord"], self.vars["wing_span"]))
			# reference point, overwritten later by CG definition
			f.write("#Xref     Yref         Zref\n")
			f.write("0         0         0\n\n")
			# profile drag estimate
			f.write("#Profile Drag\n")
			f.write("0.06\n\n")

			## Fuselage
			# create fuselage.dat file
			fuse_filename = os.path.splitext(filename)[0] + "_fuse.dat"
			self.create_fuse_file(fuse_filename)
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

# fprintf(fid, '#==============================================\n') ;%section break
# fprintf(fid, 'SURFACE\nInboard Wing\n\n'); %declare Inboard Wing
# fprintf(fid, '#NChorsewise     Spacing\n'); %source distribution
# fprintf(fid, '10            3.0\n\n');
# fprintf(fid, 'ANGLE\n%.1f\n\n', wing_incidence); %declare Wing incidence
# fprintf(fid, 'YDUPLICATE\n0.0\n\n'); %declare Wing incidence
# fprintf(fid, 'SCALE\n'); %declare Wing incidence
# fprintf(fid, '1.0    1.0    1.0\n\n'); %scaling
# fprintf(fid, 'TRANSLATE\n'); %Translation
# fprintf(fid, '0.0    0.0    0.0\n\n'); %scaling

# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence    NSpan        Spacing\n');%Section geometry
# fprintf(fid, '0    0    %.2f    %.2f        0        %i        3\n\n', fuse_diameter/2, wing_chord, np.ceil(fuse_y/0.02));
# fprintf(fid, 'NACA\n0012\n\n'); %Airfoil
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Flaps definition
# fprintf(fid, 'flap        1.0        0.7            0. 0. 0.        1.0\n\n');

# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence    NSpan        Spacing\n');%Section geometry
# fprintf(fid, '0    %.1f    %.2f    %.2f        0        %i        3\n\n', fuse_y, fuse_diameter/2, wing_chord, np.ceil(fuse_y/0.02));
# fprintf(fid, 'NACA\n0012\n\n'); %Airfoil
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Flaps definition
# fprintf(fid, 'flap        1.0        0.7            0. 0. 0.        1.0\n\n');

# fprintf(fid, '#==============================================\n') ;%section break
# fprintf(fid, 'SURFACE\nOutboard Wing\n\n'); %declare Inboard Wing
# fprintf(fid, '#NChorsewise     Spacing\n'); %source distribution
# fprintf(fid, '10            3.0\n\n');
# fprintf(fid, 'ANGLE\n%.1f\n\n', wing_incidence); %declare Wing incidence
# fprintf(fid, 'YDUPLICATE\n0.0\n\n'); %declare Wing incidence
# fprintf(fid, 'SCALE\n'); %declare Wing incidence
# fprintf(fid, '1.0    1.0    1.0\n\n'); %scaling
# fprintf(fid, 'TRANSLATE\n'); %Translation
# fprintf(fid, '0.0    0.0    0.0\n\n'); %scaling

# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence    NSpan        Spacing\n');%Section geometry
# fprintf(fid, '0    %.1f    %.2f    %.2f        0        %i        3\n\n', fuse_y, fuse_diameter/2, wing_chord, np.ceil(fuse_y/0.02));
# fprintf(fid, 'AFIL 0.0 1.0\n'); %Airfoil
# fprintf(fid, '%s\n\n', wing_airfoil);
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Flaps definition
# fprintf(fid, 'flap        1.0        0.7            0. 0. 0.        1.0\n\n');
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Flaps definition
# fprintf(fid, 'aileron        1.0        0.7            0. 0. 0.        -1.0\n\n');

# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence\n');%Section geometry
# fprintf(fid, '0    %.1f    %.2f    %.2f        0\n\n', wing_span/2, fuse_diameter/2, wing_chord);
# fprintf(fid, 'AFIL 0.0 1.0\n'); %Airfoil
# fprintf(fid, '%s\n\n', wing_airfoil);
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Flaps definition
# fprintf(fid, 'flap        1.0        0.7            0. 0. 0.        1.0\n\n');
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Flaps definition
# fprintf(fid, 'aileron        1.0        0.7            0. 0. 0.        -1.0\n\n');


# fprintf(fid, '#==============================================\n'); %section break
# fprintf(fid, 'SURFACE\nHStab\n\n'); %declare Hstab
# fprintf(fid, '#NChorsewise     Spacing\n'); %source distribution
# fprintf(fid, '10            3.0\n\n');
# fprintf(fid, 'ANGLE\n%.1f\n\n', stab_incidence); %declare Hstab incidence
# fprintf(fid, 'YDUPLICATE\n0.0\n\n'); %declare Hstab incidence
# fprintf(fid, 'SCALE\n'); %declare Hstab scale
# fprintf(fid, '1.0    1.0    1.0\n\n') ;
# fprintf(fid, 'TRANSLATE\n'); %Translation
# fprintf(fid, '0.0    0.0    0.0\n\n'); 

# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence    NSpan        Spacing\n');%Section geometry
# fprintf(fid, '%.3f    0    %.2f    %.2f        0        %i        3\n\n', htail_dist, fuse_diameter+vtail_span, htail_chord, np.ceil(htail_span/2/0.04));
# fprintf(fid, 'NACA\n0012\n\n'); %Airfoil
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Elevator definition
# fprintf(fid, 'elevator        1.0        0.7            0. 0. 0.        1.0\n\n');


# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence    NSpan        Spacing\n');%Section geometry
# fprintf(fid, '%.3f    %.3f    %.2f    %.2f        0        %i        3\n\n', htail_dist, htail_span/2, fuse_diameter+vtail_span, htail_chord, np.ceil(htail_span/2/0.04));
# fprintf(fid, 'NACA\n0012\n\n'); %Airfoil
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Elevator definition
# fprintf(fid, 'elevator        1.0        0.7            0. 0. 0.        1.0\n\n');

# fprintf(fid, '#==============================================\n'); %section break
# fprintf(fid, 'SURFACE\nVstab Left\n\n'); %declare Fin
# fprintf(fid, '#NChorsewise     Spacing\n'); %source distribution
# fprintf(fid, '10            3.0\n\n');
# fprintf(fid, 'ANGLE\n0\n\n', stab_incidence); %declare Fin incidence
# fprintf(fid, 'SCALE\n'); %Scaling
# fprintf(fid, '1.0    1.0    1.0\n\n');
# fprintf(fid, 'TRANSLATE\n'); %Translation
# fprintf(fid, '0.0    0.0    0.0\n\n');

# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence    NSpan        Spacing\n');%Section geometry
# fprintf(fid, '%.3f    %.3f    %.2f    %.2f        0        %i        3\n\n', vtail_dist, -fuse_y, fuse_diameter, vtail_chord, np.ceil(vtail_span/0.02));
# fprintf(fid, 'NACA\n0012\n\n'); %Airfoil
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %rudder definition
# fprintf(fid, 'rudder        1.0        0.7            0. 0. 0.        1.0\n\n');


# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence    NSpan        Spacing\n');%Section geometry
# fprintf(fid, '%.3f    %.3f    %.2f    %.2f        0        %i        3\n\n', vtail_dist, -fuse_y, fuse_diameter+vtail_span, vtail_chord, np.ceil(vtail_span/0.02));
# fprintf(fid, 'NACA\n0012\n\n'); %Airfoil
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Flaps definition
# fprintf(fid, 'rudder        1.0        0.7            0. 0. 0.        1.0\n\n');

# fprintf(fid, '#==============================================\n'); %section break
# fprintf(fid, 'SURFACE\nVstab Right\n\n'); %declare Fin
# fprintf(fid, '#NChorsewise     Spacing\n'); %source distribution
# fprintf(fid, '10            3.0\n\n');
# fprintf(fid, 'ANGLE\n0\n\n', stab_incidence); %declare Fin incidence
# fprintf(fid, 'SCALE\n'); %Scaling
# fprintf(fid, '1.0    1.0    1.0\n\n');
# fprintf(fid, 'TRANSLATE\n'); %Translation
# fprintf(fid, '0.0    0.0    0.0\n\n');

# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence    NSpan        Spacing\n');%Section geometry
# fprintf(fid, '%.3f    %.3f    %.2f    %.2f        0        %i        3\n\n', vtail_dist, fuse_y, fuse_diameter, vtail_chord, np.ceil(vtail_span/0.02));
# fprintf(fid, 'NACA\n0012\n\n'); %Airfoil
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %rudder definition
# fprintf(fid, 'rudder        1.0        0.7            0. 0. 0.        1.0\n\n');


# fprintf(fid, '#----------------------------------------------\n'); %surface section break
# fprintf(fid, 'SECTION\n');
# fprintf(fid, '#XLE    YLE    ZLE    Chord        Incidence    NSpan        Spacing\n');%Section geometry
# fprintf(fid, '%.3f    %.3f    %.2f    %.2f        0        %i        3\n\n', vtail_dist, fuse_y, fuse_diameter+vtail_span, vtail_chord, np.ceil(vtail_span/0.02));
# fprintf(fid, 'NACA\n0012\n\n'); %Airfoil
# fprintf(fid, 'CONTROL\n#name        gain        XHinge        XYZhvec        SgnDup\n'); %Flaps definition
# fprintf(fid, 'rudder        1.0        0.7            0. 0. 0.        1.0\n\n');
# fclose(fid);

	"""
	Creates a data file with coordinates defining the aircraft's fuselage
	Inputs:
		fuse_filename = file path to store coordinates in (should be .dat)
	"""
	def create_fuse_file(self, fuse_filename):
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
		fuse_x_arr = np.append(fuse_x_arr, np.flipud(fuse_x_arr)[1:]) # append reversed array to end, without overlapping the last point
		print("fuse_x_arr = {}".format(fuse_x_arr))

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
