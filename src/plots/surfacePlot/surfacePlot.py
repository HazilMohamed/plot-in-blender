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

def surfacePlot(z, gridMaterial, surfaceMaterial, numberMaterial):
    """
    ===========
    SURFACEPLOT
    ==========
    Surface plots are diagrams of three-dimensional data. 
    It shows a functional relationship between a designated dependent variable (z), and two independent variables (X and y).
    Arguments :
        z                   : The m*n array of values passed by user. It must be of number data type.
        gridMaterial        : The material color for grid in plot. Default color is White.
        numberMaterial      : The material color for numbers in plot. Default color is White.
        surfaceMaterial     : The material color for surface in plot. Default color is Red.
    Imported User Defined Functions :
        clearScreen         : It will delete everything on the Blender Viewport .
        textObj             : It will create a text object and convert into meshes.
        transform           : This will be used as move function for objects.
        createMaterial      : The materials were created and assigned if not exist.
    """
    # To delete default objects
    clearScreen()    
    
    # Variables used in the function.
    # X and y are obtained from length of 2D array.
    X = len(z[0])
    y = len(z)
    z_maxVal = max(list(map(max, z)))
    z_scale = math.ceil(z_maxVal/10)
    X_scale = math.ceil(X/10)
    y_scale = math.ceil(y/10)
    
    # Adding 3 2D grids for 3D space.
    create2DGrid(
        gridName="Y_Z",gridSize=10,gridLoc=(0, 0, 0), 
        gridRot=(math.radians(0), math.radians(-90), math.radians(0)), 
        x_sub=11, y_sub=11, 
        gridMaterial=gridMaterial
    )
    create2DGrid(
        gridName="X_Y",gridSize=10,gridLoc=(0, 0, 0), 
        gridRot=(math.radians(0), math.radians(0), math.radians(0)), 
        x_sub=11, y_sub=11, 
        gridMaterial=gridMaterial
    )
    create2DGrid(
        gridName="Z_X",gridSize=10,gridLoc=(0, 0, 0), 
        gridRot=(math.radians(90), math.radians(0), math.radians(0)), 
        x_sub=11, y_sub=11, 
        gridMaterial=gridMaterial
    )
    
    # Numbering X-axis, y-axis and z-axis.
    for num in range(X//X_scale):    
        textObj(
            text=int(num*X_scale), textType="X_plot", 
            textPos=((10/(X-1))*num*X_scale, -1, 0), textRot=(math.radians(0),math.radians(0) ,math.radians(90)),
            textScale=(0.4,0.4,0.4), numberMaterial=numberMaterial
        )
    for num in range(y//y_scale): 
        textObj(
            text=int(num*y_scale), textType="y_plot", 
            textPos=(0, (10/(y-1))*num*y_scale, -1), textRot=(math.radians(90),math.radians(0) ,math.radians(90)),
            textScale=(0.4,0.4,0.4), numberMaterial=numberMaterial
        )
    for num in range(11):
        textObj(
            text=int(num*z_scale), textType="z_plot", 
            textPos=(0, -1, num), textRot=(math.radians(90),math.radians(0) ,math.radians(90)),
            textScale=(0.4,0.4,0.4), numberMaterial=numberMaterial
        )
    
    # Adding grid as surface.
    bpy.ops.mesh.primitive_grid_add(size=10, location=(5,5,0),x_subdivisions=X,y_subdivisions=y)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    createMaterial(
        materialName="SurfaceMaterial", diffuseColor=surfaceMaterial
    )
    bpy.context.active_object.name = "Surface"
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_all(action = 'DESELECT')
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None
    
    # Plotting the values by moving grid vertices in given z axis.
    # First, make z in a single list.
    flat_z = [item for sublist in z for item in sublist]
    z_count = 0
    
    # Moving each vertex in Z axis. 
    for v in bm.verts: 
        v.select = True
        bpy.ops.transform.translate(value=(0, 0, flat_z[z_count]/z_scale), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        z_count += 1
        v.select = False
       
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    return

if __name__ == "__main__":
    #Json parsing.
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    surfacePlot(
        z=argv["z"],
        gridMaterial=argv["gridMaterial"], surfaceMaterial=argv["surfaceMaterial"], numberMaterial=argv["numberMaterial"]
    )