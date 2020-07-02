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

def scatterPlot2D(X, y, gridMaterial, scatterMaterial, numberMaterial):
    """
    ==============
    SCATTERPLOT 2D
    ==============
    A scatterplot in two dimenshion is used to display the relationship between two quantitative variables.
    Arguments :
        X               : The array of quantitative values passed by user. It must be of number data type.
        y               : The array of quantitative values passed by user. It must be of number data type.
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
    y_maxVal = max(y)
    X_maxVal = max(X)
    X_scale = math.ceil(X_maxVal/10)
    y_scale = math.ceil(y_maxVal/10)
    total = len(X)

    # Adding 2D grid
    create2DGrid(
        gridName="X_Y",gridSize=10,gridLoc=(0, 0, 0), 
        gridRot=(math.radians(0), math.radians(-90), math.radians(0)), 
        x_sub=11, y_sub=11, 
        gridMaterial=gridMaterial
    )
    # Numbering X-axis and y-axis
    for num in range(11):    
        textObj(
            text=int(num*y_scale), textType="y_plot", 
            textPos=(0, -1, num), textRot=(math.radians(90),math.radians(0) ,math.radians(90)),
            textScale=(0.4,0.4,0.4), numberMaterial=numberMaterial
        )
        textObj(
            text=int(num*X_scale), textType="X_plot", 
            textPos=(0, num, -1), textRot=(math.radians(90),math.radians(0),math.radians(90)),
            textScale=(0.4,0.4,0.4), numberMaterial=numberMaterial
        ) 

    # Adding a sphere in the corresponding cartesian position.
    for itr in range(total):
        # Creating a sphere.
        bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=6, radius=0.2, enter_editmode=False, align='WORLD', location=(0,X[itr]/X_scale,y[itr]/y_scale))
        bpy.context.active_object.name = "scatter "+str(itr)
        # The material will be created and applied.
        createMaterial(
            materialName="ScatterMaterial", diffuseColor=scatterMaterial
        )
        
    bpy.ops.object.select_all(action = 'DESELECT')
    return

if __name__ == "__main__":
    # Json parsing.
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    scatterPlot2D(
        X=argv["X"], y=argv["y"],
        gridMaterial=argv["gridMaterial"],scatterMaterial=argv["scatterMaterial"],numberMaterial=argv["numberMaterial"]
    )