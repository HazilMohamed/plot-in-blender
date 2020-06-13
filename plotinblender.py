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
	data = {
		"X":X,
		"y":y,
		"plotName":plotName
		}
	data = json.dumps(data)
	res = subprocess.check_output(["/usr/share/blender/blender","-P", "plots.py", "--", data])
	print(res)
