import subprocess
import math
import json
import sys

BLENDER_PATH = "/usr/share/blender/blender"					#Path to Blender file

def barPlot(X,y):
	if type(X) != list:
		X = X.tolist()
	if type(y) != list:
		y = y.tolist()
	if len(X) != len(y):
		raise IndexError("Required same number of X and y values")
	for i in y:
		if i < 0:
			raise ValueError("Negative values cannot be plotted")
	data = {
			"X":X,
			"y":y
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

def scatterPlot(X,y,z=None):
	if type(X) != list:
		X = X.tolist()
	if type(y) != list:
		y = y.tolist()
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
			"z":z
		}
		data = json.dumps(data)
		try:
			res = subprocess.Popen([BLENDER_PATH,"-P", "src/plots/scatterPlot/scatterPlot3D.py", "--", data],
				stdout=subprocess.PIPE) 
			output = res.communicate()
			print(output)
		except OSError as e:
			raise OSError(str(e))	
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
			"y":y
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

def histPlot(X,bins=None):
	if type(X) != list:
		X = X.tolist()
	if bins is not None and type(bins) != int:
		raise TypeError("invalid data type bin")
	if bins is not None and bins > len(X):
		raise IOError("bins cannot be greater than total length")
	for i in X:
		if type(i) not in [int,float]:
			raise TypeError("Only numbers can be plotted")
		if i < 0:
			#TODO:
			#Supporting negative values too
			raise ValueError("Negative values cannot be plotted")
	data = {
			"X":X,
			"bins":bins
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

def surfacePlot(z):
	length = len(z[0])
	if type(z) != list:
		z = z.tolist()
	for l in z:
		if len(l) != length:
			raise ValueError("Same number of elements required in each row")
		if not isinstance(l,list):
			raise TypeError("Required a 2D array")
		for i in l:
			if type(i) not in [int,float]:
				raise TypeError("Only numbers can be plotted")	
	data = {
			"z":z
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

	

