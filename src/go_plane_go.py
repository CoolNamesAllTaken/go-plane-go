import numpy as np 
import matplotlib.pyplot as plt 

# Import our own neato files
from plane_geometry import PlaneGeometry

# for testing only
from utils import *

# NOTE: this program MUST be run from the go-plane-go directory

def main():
	print(parse_text_file("config/test_parser.txt"))
	# our_plane = PlaneGeometry("config/test_parser.txt")

if __name__ == "__main__":
	main()