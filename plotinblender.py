import subprocess
import math
import json
import sys

BLENDER_PATH = "/usr/share/blender/blender"					#Path to Blender file

def barPlot(X=None, y=None, barMaterial=(1,0,0,1), numberMaterial=(1,1,1,1), gridMaterial=(1,1,1,1)):
	if X is None or y is None:
		raise TypeError("Must pass both X and y")

	if type(X) != list:
		X = X.tolist()
	
	if type(y) != list:
		y = y.tolist()
	
	if len(X) != len(y):
		raise IndexError("Required same number of X and y values")

	for i in [barMaterial, numberMaterial, gridMaterial]:
		if len(i) != 4:
			raise IOError("The material arguments value tuple in the format (R,G,B,A)")
		for j in i:
			if type(j) not in [int, float] or j < 0:
				raise ValueError("Only positive numbers can be used in material")
	
	for i in y:
		if i < 0:
			raise ValueError("Negative values cannot be plotted")
	
	data = {
			"X":X,
			"y":y,
			"barMaterial":barMaterial,
			"gridMaterial":gridMaterial,
			"numberMaterial":numberMaterial
		}
	data = json.dumps(data)
	
	try:
		res = subprocess.Popen([BLENDER_PATH,"-P", "src/plots/barPlot/barPlot.py", "--", data],
			stdout=subprocess.PIPE) 
		output = res.communicate()
		print(output)
	except OSError as e:
		raise OSError(str(e))	
	return

def scatterPlot(X=None, y=None, z=None, scatterMaterial=(1,0,0,1), numberMaterial=(1,1,1,1), gridMaterial=(1,1,1,1)):
	if X is None or y is None:
		raise TypeError("Must pass both X and y")
	if type(X) != list:
		X = X.tolist()
	
	if type(y) != list:
		y = y.tolist()
	
	for i in [scatterMaterial, numberMaterial, gridMaterial]:
		if len(i) != 4:
			raise IOError("The material arguments value tuple in the format (R,G,B,A)")
		for j in i:
			if type(j) not in [int, float] or j < 0:
				raise ValueError("Only positive numbers can be used in material")
	
	#validation for 3D scatterPlot
	if z is not None:
		if type(z) != list:
			z = z.tolist()	
		if len(X) != len(y) or len(y) != len(z):
			raise IndexError("Required same number of X, y and z values")
		for i in X,y,z:
			for j in i:		
				if type(j) not in [int,float]:
					raise TypeError("Only numbers can be plotted")
				if j < 0:
					#TODO:
					#Supporting negative values too
					raise ValueError("Negative values cannot be plotted")
		data = {
			"X":X,
			"y":y,
			"z":z,
			"scatterMaterial":scatterMaterial,
			"gridMaterial":gridMaterial,
			"numberMaterial":numberMaterial			
		}
		data = json.dumps(data)
		try:
			res = subprocess.Popen([BLENDER_PATH,"-P", "src/plots/scatterPlot/scatterPlot3D.py", "--", data],
				stdout=subprocess.PIPE) 
			output = res.communicate()
			print(output)
		except OSError as e:
			raise OSError(str(e))	
	
	#validation for 2D scatterPlot
	else:
		if len(X) != len(y):
			raise IndexError("Required same number of X and y values")
		
		for i in X,y:
			for j in i:
				if type(j) not in [int,float]:
					raise TypeError("Only numbers can be plotted")
				if j < 0:
					#TODO:
					#Supporting negative values too
					raise ValueError("Negative values cannot be plotted")
		
		data = {
			"X":X,
			"y":y,
			"scatterMaterial":scatterMaterial,
			"gridMaterial":gridMaterial,
			"numberMaterial":numberMaterial				
		}
		data = json.dumps(data)
		
		try:
			res = subprocess.Popen([BLENDER_PATH,"-P", "src/plots/scatterPlot/scatterPlot2D.py", "--", data],
				stdout=subprocess.PIPE) 
			output = res.communicate()
			print(output)
		except OSError as e:
			raise OSError(str(e))
	return

def histPlot(X=None, bins=None, cat=None, numberMaterial=(1,1,1,1), gridMaterial=(1,1,1,1)):
	if X is None:
		raise ValueError("Must pass X")

	if type(X) != list:
		X = X.tolist()
	
	if bins is not None and type(bins) != int:
		raise TypeError("invalid data type bin")
	
	if bins is not None and bins > len(X):
		raise IOError("bins cannot be greater than total length")
	
	for i in [numberMaterial, gridMaterial]:
		if len(i) != 4:
			raise IOError("The material arguments value tuple in the format (R,G,B,A)")
		for j in i:
			if type(j) not in [int, float] or j < 0:
				raise ValueError("Only positive numbers can be used in material")
		
	for i in X:
		if type(i) not in [int,float]:
			raise TypeError("Only numbers can be plotted")
		if i < 0:
			#TODO:
			#Supporting negative values too
			raise ValueError("Negative values cannot be plotted")
		
	if cat is not None:
		if type(cat) != list:
			cat = cat.tolist()
		if len(cat) != len(X):
			raise ValueError("Required same number of lengths")
	if cat is None:
		cat = [1]*len(X)
	
	if len(set(cat)) > 8:
		raise ValueError("cat can take up to 8 values")
	
	newX = []
	newX.extend([list(a) for a in zip(X, cat)])

	data = {
			"X":newX,
			"bins":bins,
			"cat":cat,
			"gridMaterial":gridMaterial,
			"numberMaterial":numberMaterial
		}
	data = json.dumps(data)
	
	try:
		res = subprocess.Popen([BLENDER_PATH,"-P", "src/plots/histPlot/histPlot.py", "--", data],
			stdout=subprocess.PIPE) 
		output = res.communicate()
		print(output)
	except OSError as e:
		raise OSError(str(e))
	return

def surfacePlot(z=None, surfaceMaterial=(1,0,0,1), numberMaterial=(1,1,1,1), gridMaterial=(1,1,1,1)):
	if z is None:
		raise ValueError("Must pass z")
	
	length = len(z[0])
	if type(z) != list:
		z = z.tolist()
	
	for i in [surfaceMaterial, numberMaterial, gridMaterial]:
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
			"surfaceMaterial":surfaceMaterial,
			"gridMaterial":gridMaterial,
			"numberMaterial":numberMaterial
		}
	data = json.dumps(data)
	
	try:
		res = subprocess.Popen([BLENDER_PATH,"-P", "src/plots/surfacePlot/surfacePlot.py", "--", data],
			stdout=subprocess.PIPE) 
		output = res.communicate()
		print(output)
	except OSError as e:
		raise OSError(str(e))
	return

	

