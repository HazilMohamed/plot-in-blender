import subprocess
import math
import json

plots = ["barPlot","scatterPlot"]					#Available Plots go here
BLENDER_PATH = "/usr/share/blender/blender"			#Path to Blender file

def plot(X,y,plotName):
	if type(X) != list:
		X = X.tolist()
	if type(y) != list:
		y = y.tolist()
	if plotName not in plots:
		raise ValueError("Plot not available")
	if len(X) != len(y):
		raise IndexError("Required same number of X and y values")
	isValid = validate(X,y,plotName)
	if isValid:
		data = {
			"X":X,
			"y":y,
			"plotName":plotName
			}
		data = json.dumps(data)
		try:
			res = subprocess.check_output([BLENDER_PATH,"-P", "plots.py", "--", data])
			print(res)
		except OSError as e:
			raise OSError(str(e))	
	return

def validate(X,y,plotName):
	isValid = True
	if plotName == "barPlot":
		for i in y:
			if i < 0:
				isValid = False
				raise ValueError("Negative values cannot be plotted")
	elif plotName == "scatterPlot":
		for i in X,y:
			for j in i:
				if type(j) != (int or float):
					isValid = False
					raise TypeError("Only numbers can be plotted")
				if j < 0:
					#TODO:
					#Supporting negative values too
					isValid = False
					raise ValueError("Negative values cannot be plotted")
	return isValid