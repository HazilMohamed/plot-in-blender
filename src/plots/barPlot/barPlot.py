import bpy
import bmesh
import math
import sys
import json

sys.path.append("src/tools/")

from create2DGrid import create2DGrid
from textObj import textObj
from transform import transform
from clearScreen import clearScreen

def barPlot(X,y):
    #To delete default objects
    clearScreen()
    
    #local variables
    maxVal = max(y)
    total = len(X)
    X_scale = 10/total
    y_scale = math.ceil(maxVal/10)
    size_bar = 1
    cursor = size_bar/2

    #adding 2D grid 0.01 is used to push grid little back else face mix will happen
    create2DGrid("X_Y", 10, (-(size_bar/2)+0.01, 0, 0), (math.radians(0), math.radians(-90), math.radians(0)), 11, 2)

    #numbering y-axis
    for num in range(11):    
        textObj(num*y_scale, "y_plot", (-(size_bar/2), -1, num), (math.radians(90),math.radians(0) ,math.radians(90)))

    #plotting and naming x axis
    for itr in range(total):
        #initilializing a plane
        bpy.ops.mesh.primitive_plane_add(size=size_bar, enter_editmode=False, location=(0, cursor, 0))
        bpy.context.active_object.name = "Bar "+str(X[itr])
        
        #scaling bar plots
        transform('EDIT', 'EDGE', size_bar, X_scale, [2,3]) #[2,3] reps rhs of plane from user perspective
        
        #extruding plane along z axis
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type = 'FACE')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, y[itr]/y_scale)}
        )
        bpy.ops.object.mode_set( mode = 'OBJECT' )
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        textObj(X[itr], "X_plot", (0, (X_scale-size_bar)/2+cursor, -1), (math.radians(90),math.radians(90),math.radians(90)),(min(1,X_scale), min(1,X_scale), min(1,X_scale))) 
        cursor += X_scale

    bpy.ops.object.select_all(action = 'DESELECT')
    return


if __name__ == "__main__":
    #Json parsing
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    barPlot(argv["X"],argv["y"])