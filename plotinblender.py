import subprocess
import math
import json
import sys
import os

# Importing BLENDER_PATH from environemnt variables
BLENDER_PATH = os.environ.get("BLENDER_PATH")

if BLENDER_PATH is None:
	raise OSError("Export BLENDER_PATH to env")

if not os.path.isfile(BLENDER_PATH):
	raise FileNotFoundError("Blender not found")

def barplot(x=None, y=None, bar_material=(1,0,0,1), 
			number_material=(1,1,1,1), grid_material=(1,1,1,1)):
	if x is None or y is None:
		raise TypeError("Must pass both x and y")

	if type(x) != list:
		x = x.tolist()
	
	if type(y) != list:
		y = y.tolist()
	
	if len(x) != len(y):
		raise IndexError("Required same number of x and y values")

	for i in [bar_material, number_material, grid_material]:
		if len(i) != 4:
			raise IOError("The material arguments value tuple in the format (R,G,B,A)")
		for j in i:
			if type(j) not in [int, float] or j < 0:
				raise ValueError("Only positive numbers can be used in material")
	
	for i in y:
		if i < 0:
			raise ValueError("Negative values cannot be plotted")
	
	data = {
			"x":x,
			"y":y,
			"bar_material":bar_material,
			"grid_material":grid_material,
			"number_material":number_material
		}
	data = json.dumps(data)
	
	try:
		res = subprocess.Popen(
				[BLENDER_PATH,"-P", "src/plots/barplot/barplot.py", "--", data],
				stdout=subprocess.PIPE) 
		output = res.communicate()
		print(output)
	except OSError as e:
		raise OSError(str(e))	
	return

def scatterplot(x=None, y=None, z=None, cat=None, 
				number_material=(1,1,1,1), grid_material=(1,1,1,1)):
	if x is None or y is None:
		raise TypeError("Must pass both x and y")
	if type(x) != list:
		x = x.tolist()
	
	if type(y) != list:
		y = y.tolist()
	
	for i in [number_material, grid_material]:
		if len(i) != 4:
			raise IOError("The material arguments value tuple in the format (R,G,B,A)")
		for j in i:
			if type(j) not in [int, float] or j < 0:
				raise ValueError("Only positive numbers can be used in material")
	
	if cat is not None:
		if type(cat) != list:
			cat = cat.tolist()
		if len(cat) != len(x):
			raise ValueError("Required same number of lengths")
	
	if cat is None:
		cat = [1]*len(x)
	
	if len(set(cat)) > 8:
		raise ValueError("cat can take up to 8 values")

	# Validation for 3D scatterplot
	if z is not None:
		if type(z) != list:
			z = z.tolist()	
		if len(x) != len(y) or len(y) != len(z):
			raise IndexError("Required same number of x, y and z values")
		for i in x,y,z:
			for j in i:		
				if type(j) not in [int,float]:
					raise TypeError("Only numbers can be plotted")
				if j < 0:
					# TODO:
					# Supporting negative values too
					raise ValueError("Negative values cannot be plotted")
		data = {
			"x":x,
			"y":y,
			"z":z,
			"cat":cat,
			"grid_material":grid_material,
			"number_material":number_material			
		}
		data = json.dumps(data)
		try:
			res = subprocess.Popen(
					[BLENDER_PATH,"-P", "src/plots/scatterplot/scatterplot3D.py", "--", data],
					stdout=subprocess.PIPE) 
			output = res.communicate()
			print(output)
		except OSError as e:
			raise OSError(str(e))	
	
	# Validation for 2D scatterplot
	else:
		if len(x) != len(y):
			raise IndexError("Required same number of x and y values")
		
		for i in x,y:
			for j in i:
				if type(j) not in [int,float]:
					raise TypeError("Only numbers can be plotted")
				if j < 0:
					# TODO:
					# Supporting negative values too
					raise ValueError("Negative values cannot be plotted")
		
		data = {
			"x":x,
			"y":y,
			"cat":cat,
			"grid_material":grid_material,
			"number_material":number_material				
		}
		data = json.dumps(data)
		
		try:
			res = subprocess.Popen(
					[BLENDER_PATH,"-P", "src/plots/scatterplot/scatterplot2D.py", "--", data],
					stdout=subprocess.PIPE) 
			output = res.communicate()
			print(output)
		except OSError as e:
			raise OSError(str(e))
	return

def histplot(x=None, bins=None, cat=None, 
			 number_material=(1,1,1,1), grid_material=(1,1,1,1)):
	if x is None:
		raise ValueError("Must pass x")

	if type(x) != list:
		x = x.tolist()
	
	if bins is not None and type(bins) != int:
		raise TypeError("invalid data type bin")
	
	if bins is not None and bins > len(x):
		raise IOError("bins cannot be greater than total length")
	
	for i in [number_material, grid_material]:
		if len(i) != 4:
			raise IOError("The material arguments value tuple in the format (R,G,B,A)")
		for j in i:
			if type(j) not in [int, float] or j < 0:
				raise ValueError("Only positive numbers can be used in material")
		
	for i in x:
		if type(i) not in [int,float]:
			raise TypeError("Only numbers can be plotted")
		if i < 0:
			# TODO:
			# Supporting negative values too
			raise ValueError("Negative values cannot be plotted")
		
	if cat is not None:
		if type(cat) != list:
			cat = cat.tolist()
		if len(cat) != len(x):
			raise ValueError("Required same number of lengths")
	if cat is None:
		cat = [1]*len(x)
	
	if len(set(cat)) > 8:
		raise ValueError("cat can take up to 8 values")
	
	data = {
			"x":x,
			"bins":bins,
			"cat":cat,
			"grid_material":grid_material,
			"number_material":number_material
		}
	data = json.dumps(data)
	
	try:
		res = subprocess.Popen(
				[BLENDER_PATH,"-P", "src/plots/histplot/histplot.py", "--", data],
				stdout=subprocess.PIPE) 
		output = res.communicate()
		print(output)
	except OSError as e:
		raise OSError(str(e))
	return

def surfaceplot(z=None, surface_material=(1,0,0,1), 
				number_material=(1,1,1,1), grid_material=(1,1,1,1)):
	if z is None:
		raise ValueError("Must pass z")
	
	length = len(z[0])
	if type(z) != list:
		z = z.tolist()
	
	for i in [surface_material, number_material, grid_material]:
		if len(i) != 4:
			raise IOError("The material arguments value tuple in the format (R,G,B,A)")
		for j in i:
			if type(j) not in [int, float] or j < 0:
				raise ValueError("Only positive numbers can be used in material")
	
	for l in z:
		if len(l) != length:
			raise ValueError("Same number of elements required in each row")
		if not isinstance(l,list):
			raise TypeError("Required a 2D array")
		for i in l:
			if type(i) not in [int,float]:
				raise TypeError("Only numbers can be plotted")	
	
	data = {
			"z":z,
			"surface_material":surface_material,
			"grid_material":grid_material,
			"number_material":number_material
		}
	data = json.dumps(data)
	
	try:
		res = subprocess.Popen(
				[BLENDER_PATH,"-P", "src/plots/surfaceplot/surfaceplot.py", "--", data],
				stdout=subprocess.PIPE) 
		output = res.communicate()
		print(output)
	except OSError as e:
		raise OSError(str(e))
	return

def pieplot(x=None,y=None):
	if x is None or y is None:
		raise TypeError("Must pass both x and y") 
	
	if type(x) != list:
		x = x.tolist()
	
	if type(y) != list:
		y = y.tolist()
	
	if len(x) != len(y):
		raise IndexError("Required same number of x and y values")
	
	for i in x:
		if i < 0:
			raise ValueError("Negative values cannot be used in pieplots")
	
	data = {
			"x":x,
			"y":y
		}
	data = json.dumps(data)
	
	try:
		res = subprocess.Popen(
				[BLENDER_PATH,"-P", "src/plots/pieplot/pieplot.py", "--", data],
				stdout=subprocess.PIPE) 
		output = res.communicate()
		print(output)
	except OSError as e:
		raise OSError(str(e))	
	return