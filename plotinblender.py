import subprocess
import math
import json

plots = ["barPlot","scatterPlot"]									#Available Plots go here
BLENDER_PATH = "/usr/share/blender/blender"							#Path to Blender file

def plot(X, y, plotName, z=None):
	if type(X) != list:
		X = X.tolist()
	if type(y) != list:
		y = y.tolist()
	if z is not None:
		if type(z) != list:
			z = z.tolist()
	if plotName not in plots:
		raise ValueError("Plot not available")
	isValid, plotName = validate(X, y, plotName, z)
	if isValid:
		data = {
			"X":X,
			"y":y,
			"z":z,
			"plotName":plotName
			}
		data = json.dumps(data)
		try:
			res = subprocess.check_output([BLENDER_PATH,"-P", "ploting.py", "--", data])
			print(res)
		except OSError as e:
			raise OSError(str(e))	
	return

def validate(X, y, plotName, z=None):
	isValid = True
	if plotName == "barPlot":
		if z is not None:
			raise TypeError("Z cannot be plotted")
		if len(X) != len(y):
			raise IndexError("Required same number of X and y values")
		for i in y:
			if i < 0:
				isValid = False
				raise ValueError("Negative values cannot be plotted")
	elif plotName == "scatterPlot":
		if type(z) == list:
			if len(X) != len(y) or len(y) != len(z):
				raise IndexError("Required same number of X, y and z values")
			for i in X,y,z:
				for j in i:		
					if type(j) not in [int,float]:
						isValid = False
						raise TypeError("Only numbers can be plotted")
					if j < 0:
						#TODO:
						#Supporting negative values too
						isValid = False
						raise ValueError("Negative values cannot be plotted")
			plotName = plotName + "3D"
		else:
			if len(X) != len(y):
				raise IndexError("Required same number of X and y values")
			for i in X,y:
				for j in i:
					if type(j) not in [int,float]:
						isValid = False
						raise TypeError("Only numbers can be plotted")
					if j < 0:
						#TODO:
						#Supporting negative values too
						isValid = False
						raise ValueError("Negative values cannot be plotted")
			plotName = plotName + "2D"
		

	return isValid,plotName