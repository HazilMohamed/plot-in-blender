import subprocess
import math
import json

plots = ["barPlot","scatterPlot"]

def plot(X,y,plotName):
	if type(X) != list:
		X = X.tolist()
	if type(y) != list:
		y = y.tolist()
	if plotName not in plots:
		print("Plot not available")
		return
	if len(X) != len(y):
		print("Required same number of X and y")
		return
	isValid = validate(X,y,plotName)
	if isValid:
		data = {
			"X":X,
			"y":y,
			"plotName":plotName
			}
		data = json.dumps(data)
		res = subprocess.check_output(["/usr/share/blender/blender","-P", "plots.py", "--", data])
		print(res)
	return

def validate(X,y,plotName):
	isValid = True
	if plotName == "barPlot":
		for i in y:
			if i < 0:
				print("Negative values cannot be plotted")
				isValid = False
				return
	elif plotName == "scatterPlot":
		for i in X,y:
			for j in i:
				if type(j) != (int or float):
					print("Only numbers can be plotted")
					isValid = False
					return
				if j < 0:
					print("Negative values cannot be plotted")
					isValid = False
					return
	return isValid