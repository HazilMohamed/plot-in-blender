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

def scatterPlot3D(X, y, z, gridMaterial, scatterMaterial, numberMaterial):
    """
    ==============
    SCATTERPLOT 3D
    ==============
    A scatterplot in three dimenshion is used to display the relationship between three quantitative variables.
    Arguments :
        X               : The array of quantitative values passed by user. It must be of number data type.
        y               : The array of quantitative values passed by user. It must be of number data type.
        z               : The array of quantitative values passed by user. It must be of number data type.
        gridMaterial    : The material color for grid in plot. Default color is White.
        numberMaterial  : The material color for numbers in plot. Default color is White.
        scatterMaterial : The material color for scatters in plot. Default color is Red.
    Imported User Defined Functions :
        clearScreen     : It will delete everything on the Blender Viewport .
        textObj         : It will create a text object and convert into meshes.
        transform       : This will be used as move function for objects.
        createMaterial  : The materials were created and assigned if not exist.
    """
    # Delete everything on the screen.
    clearScreen()
    
    # Variables used in the function.
    X_maxVal = max(X)
    y_maxVal = max(y)
    z_maxVal = max(z)
    X_scale = math.ceil(X_maxVal/10)
    y_scale = math.ceil(y_maxVal/10)
    z_scale = math.ceil(z_maxVal/10)
    total = len(X)

    # Adding 3D grid by combining 3 2D grids.
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
    for num in range(11):    
        textObj(
            text=int(num*X_scale), textType="X_plot", 
            textPos=(num, -1, 0), textRot=(math.radians(0),math.radians(0) ,math.radians(90)),
            textScale=(0.4,0.4,0.4), numberMaterial=numberMaterial
        )
        textObj(
            text=int(num*y_scale), textType="y_plot", 
            textPos=(0, num, -1), textRot=(math.radians(90),math.radians(0) ,math.radians(90)),
            textScale=(0.4,0.4,0.4), numberMaterial=numberMaterial
        )
        textObj(
            text=int(num*z_scale), textType="z_plot", 
            textPos=(0, -1, num), textRot=(math.radians(90),math.radians(0) ,math.radians(90)),
            textScale=(0.4,0.4,0.4), numberMaterial=numberMaterial
        )
    # Adding a sphere in the corresponding cartesian position.
    for itr in range(total):
        # Creating a sphere.
        bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=6, radius=0.2, enter_editmode=False, align='WORLD', location=(X[itr]/X_scale,y[itr]/y_scale,z[itr]/z_scale))
        bpy.context.active_object.name = "scatter "+str(itr)
        # The material will be created and applied.
        createMaterial(
            materialName="ScatterMaterial",diffuseColor=scatterMaterial
        )
        
    bpy.ops.object.select_all(action = 'DESELECT')
    return

if __name__ == "__main__":
    #Json parsing.
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    scatterPlot3D(
        X=argv["X"], y=argv["y"], z=argv["z"],
        gridMaterial=argv["gridMaterial"], scatterMaterial=argv["scatterMaterial"], numberMaterial=argv["numberMaterial"]    
    )