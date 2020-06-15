import bpy
import bmesh
import math
import sys

from create2DGrid import create2DGrid
from textObj import textObj
from transform import transform

def histPlot(X):
    
    #local variables
    X.sort()
    maxVal = X[-1]
    minVal = X[0]
    bins = math.ceil(math.sqrt(len(X)))
    binWidth = math.ceil((maxVal-minVal)/bins)
    hist = 0 
    count = 0
    X_new = []
    y_new = []
    size_bar = 1
    cursor = size_bar/2
    
    X_new = list(range(math.ceil(minVal-1),math.ceil(maxVal),binWidth))
    current = binWidth
    while count < len(X):
        if X[count] <= current:
            hist += 1
            count += 1
        else:
            y_new.append(hist)
            current += binWidth
            hist = 0 
    y_new.append(hist)
    y_scale = math.ceil(max(y_new)/10)
    X_scale = 10/len(X_new)
    
    #adding 2D grid 0.01 is used to push grid little back else face mix will happen
    create2DGrid("X-Y",10,(-(size_bar/2)+0.01, 0, 0),(math.radians(0), math.radians(-90), math.radians(0)),11,2)

    #numbering y-axis
    for num in range(11):    
        textObj(num*y_scale, "y_plot", (-(size_bar/2), -1, num), (math.radians(90),math.radians(0) ,math.radians(90)))

    #plotting and naming x axis
    for itr in range(len(X_new)):
        #initilializing a plane
        bpy.ops.mesh.primitive_plane_add(size=size_bar, enter_editmode=False, location=(0, cursor, 0))
        bpy.context.active_object.name = "Bar "+str(X_new[itr])
        
        #scaling bar plots
        transform('EDIT', 'EDGE', size_bar, X_scale, [2,3]) #[2,3] reps rhs of plane from user perspective
        
        #extruding plane along z axis
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type = 'FACE')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, y_new[itr]/y_scale)}
        )
        bpy.ops.object.mode_set( mode = 'OBJECT' )
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        textObj(X_new[itr], "X_plot", (0, X_scale*itr, -1), (math.radians(90),math.radians(0),math.radians(90)),(min(1,X_scale/2), min(1,X_scale/2), min(1,X_scale/2))) 
        cursor += X_scale
    textObj(max(X_new)+binWidth, "X_plot", (0, 10, -1), (math.radians(90),math.radians(0),math.radians(90)),(min(1,X_scale/2), min(1,X_scale/2), min(1,X_scale/2)))    
    bpy.ops.object.select_all(action = 'DESELECT')
    return