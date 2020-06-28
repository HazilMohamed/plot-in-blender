import bpy
import math
import sys
import json

sys.path.append("src/tools/")

from create2DGrid import create2DGrid
from textObj import textObj
from transform import transform
from clearScreen import clearScreen
from createMaterial import createMaterial

def scatterPlot2D(X,y):
    #To delete default objects
    clearScreen()
    
    #local variables
    y_maxVal = max(y)
    X_maxVal = max(X)
    X_scale = math.ceil(X_maxVal/10)
    y_scale = math.ceil(y_maxVal/10)
    total = len(X)

    #adding 2D grid
    create2DGrid("X-Y", 10, (0, 0, 0), (math.radians(0), math.radians(-90), math.radians(0)), 11, 11)

    #numbering y-axis and X-axis
    for num in range(11):    
        textObj(int(num*y_scale), "y_plot", (0, -1, num), (math.radians(90),math.radians(0) ,math.radians(90)),textScale=(0.4,0.4,0.4))
        textObj(int(num*X_scale), "X_plot", (0, num, -1), (math.radians(90),math.radians(0),math.radians(90)),textScale=(0.4,0.4,0.4)) 

    #plotting
    for itr in range(total):
        #plotting sphere
        bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=6, radius=0.2, enter_editmode=False, align='WORLD', location=(0,X[itr]/X_scale,y[itr]/y_scale))
        bpy.context.active_object.name = "scatter "+str(itr)
        createMaterial("ScatterMaterial",(3,1,7,1))
        
    bpy.ops.object.select_all(action = 'DESELECT')
    return

if __name__ == "__main__":
    #Json parsing
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    scatterPlot2D(argv["X"],argv["y"])