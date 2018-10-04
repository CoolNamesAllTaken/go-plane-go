import numpy as np 
import matplotlib.pyplot as plt 

# Import our own neato files
from plane_geometry import PlaneGeometry

def main():
	print("Hello World!")
	our_plane = PlaneGeometry("poopy potato")
	our_plane.hello_world();

if __name__ == "__main__":
	main()