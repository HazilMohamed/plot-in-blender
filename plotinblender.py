import subprocess
import math

def plot(X,y,plotName):
    X_str = ""
    y_str = ""
    for elt in X:
	    X_str = X_str + elt + "//" 
    X_str = X_str[:-2]   
    for val in y:
	    y_str = y_str + str(math.ceil(val)) + "//"
    y_str = y_str[:-2]
    res = subprocess.check_output(["/usr/share/blender/blender", "-P", "plots.py", "--", X_str, y_str, plotName])
