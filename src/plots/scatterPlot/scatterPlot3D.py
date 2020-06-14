import bpy
import math

from create2DGrid import create2DGrid
from textObj import textObj
from transform import transform

def scatterPlot3D(X,y,z):
    
    #local variables
    X_maxVal = max(X)
    y_maxVal = max(y)
    z_maxVal = max(z)
    X_scale = math.ceil(X_maxVal/10)
    y_scale = math.ceil(y_maxVal/10)
    z_scale = math.ceil(z_maxVal/10)
    total = len(X)

    #adding 3D grid
    create2DGrid("Y-Z", 10, (0, 0, 0), (math.radians(0), math.radians(-90), math.radians(0)), 11, 11)
    create2DGrid("X-Y", 10, (0, 0, 0), (math.radians(0), math.radians(0), math.radians(0)), 11, 11)
    create2DGrid("Z-X", 10, (0, 0, 0), (math.radians(90), math.radians(0), math.radians(0)), 11, 11)

    #numbering X-axis, y-axis and z-axis
    for num in range(11):    
        textObj(int(num*X_scale), "X_plot", (num, -1, 0), (math.radians(0),math.radians(0),math.radians(90)),textScale=(0.4,0.4,0.4))
        textObj(int(num*y_scale), "y_plot", (0, num, -1), (math.radians(90),math.radians(0) ,math.radians(90)),textScale=(0.4,0.4,0.4)) 
        textObj(int(num*z_scale), "z_plot", (0, -1, num), (math.radians(90),math.radians(0),math.radians(90)),textScale=(0.4,0.4,0.4))
    
    #plotting
    for itr in range(total):
        #plotting sphere
        bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=6, radius=0.2, enter_editmode=False, align='WORLD', location=(X[itr]/X_scale,y[itr]/y_scale,z[itr]/z_scale))

        bpy.context.active_object.name = "scatter "+str(itr)
        
    bpy.ops.object.select_all(action = 'DESELECT')