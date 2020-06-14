import bpy
import math
import sys
import json

#Available Plots
plots2D = ["barPlot","scatterPlot2D"]
plots3D = ["scatterPlot3D"]

#Paths
sys.path.append('src/plots/barPlot/')
sys.path.append('src/plots/scatterPlot')
sys.path.append('src/tools/')

#Importing plots
from barPlot import barPlot
from scatterPlot2D import scatterPlot2D
from scatterPlot3D import scatterPlot3D
 
def init():
    
    #deleting previous
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()

    #json data values
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    if argv["plotName"] in plots2D:
        eval(argv["plotName"])(argv["X"],argv["y"])
    elif argv["plotName"] in plots3D:
        eval(argv["plotName"])(argv["X"],argv["y"],argv["z"])
        
if __name__ == "__main__":
    init()
