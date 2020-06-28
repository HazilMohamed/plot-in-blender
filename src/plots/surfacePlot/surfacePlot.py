import bpy
import bmesh
import sys
import math
import json

sys.path.append("src/tools/")

from create2DGrid import create2DGrid
from textObj import textObj
from transform import transform
from clearScreen import clearScreen
from createMaterial import createMaterial

def surfacePlot(z):
    #To delete default objects
    clearScreen()    
    
    #X and y are obtained from length of 2D array
    X = len(z[0])
    y = len(z)
    z_maxVal = max(list(map(max, z)))
    z_scale = math.ceil(z_maxVal/10)
    X_scale = math.ceil(X/10)
    y_scale = math.ceil(y/10)
    
    #adding 3 2D grids for 3D space
    create2DGrid("Y-Z", 10, (0, 0, 0), (math.radians(0), math.radians(-90), math.radians(0)), 11, 11)
    create2DGrid("X-Y", 10, (0, 0, 0), (math.radians(0), math.radians(0), math.radians(0)), 11, 11)
    create2DGrid("Z-X", 10, (0, 0, 0), (math.radians(90), math.radians(0), math.radians(0)), 11, 11)
    
    #numbering X-axis, y-axis and z-axis
    for num in range(X//X_scale):    
        textObj(int(num*X_scale), "X_plot", ((10/(X-1))*num*X_scale, -1, 0), (math.radians(0),math.radians(0),math.radians(90)),textScale=(0.4,0.4,0.4))
    for num in range(y//y_scale): 
        textObj(int(num*y_scale), "y_plot", (0, (10/(y-1))*num*y_scale, -1), (math.radians(90),math.radians(0) ,math.radians(90)),textScale=(0.4,0.4,0.4))
    for num in range(11): 
        textObj(int(num*z_scale), "z_plot", (0, -1, num), (math.radians(90),math.radians(0),math.radians(90)),textScale=(0.4,0.4,0.4))
    
    #Adding surface
    bpy.ops.mesh.primitive_grid_add(size=10, location=(5,5,0),x_subdivisions=X,y_subdivisions=y)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    createMaterial("SurfaceMaterial",(7,4,4,1))
    bpy.context.active_object.name = "Surface"
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_all(action = 'DESELECT')
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None
    
    #plotting
    #First, make z in a single list
    flat_z = [item for sublist in z for item in sublist]
    z_count = 0
    #moving each vertex in Z axis 
    for v in bm.verts: 
        v.select = True
        bpy.ops.transform.translate(value=(0, 0, flat_z[z_count]/z_scale), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        z_count += 1
        v.select = False
       
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    return

if __name__ == "__main__":
    #Json parsing
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    surfacePlot(argv["z"])