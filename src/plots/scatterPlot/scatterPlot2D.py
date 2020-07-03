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

def scatterPlot2D(X, y, cat, gridMaterial, numberMaterial):
    """
    ==============
    SCATTERPLOT 2D
    ==============
    A scatterplot in two dimenshion is used to display the relationship between two quantitative variables.
    Arguments :
        X               : The array of quantitative values passed by user. It must be of number data type.
        y               : The array of quantitative values passed by user. It must be of number data type.
        cat             : The array of categorical values respected to each value in (X,y).  
        gridMaterial    : The material color for grid in plot. Default color is White.
        numberMaterial  : The material color for numbers in plot. Default color is White.
    Imported User Defined Functions :
        clearScreen     : It will delete everything on the Blender Viewport .
        textObj         : It will create a text object and convert into meshes.
        transform       : This will be used as move function for objects.
        createMaterial  : The materials were created and assigned if not exist.
    """

    # 8 colors are declared right now for to use, every material is diffuse material in Blender
    scatterMaterial = [
        ("red",(1,0,0,1)),("yellow",(1,1,0,1)),("blue",(0,0,1,1)),
        ("green",(0,1,0,1)),("cyan",(0,1,1,1)),("purple",(1,0,1,1)),
        ("magenda",(1,0,0.25,1),("orange",(1,0.25,0,1)))
    ]

    # Delete everything on the screen.
    clearScreen()
    
    # Variables used in the function.
    X_y_cat = []
    X_y_cat.extend([list(a) for a in zip(X, y, cat)])
    y_maxVal = max(y)
    X_maxVal = max(X)
    X_scale = math.ceil(X_maxVal/10)
    y_scale = math.ceil(y_maxVal/10)
    total = len(X)
    categories = list(set(cat))

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
    for i in range(len(categories)):
        for itr in range(total):
            if categories[i] == X_y_cat[itr][-1]:
                # Creating a sphere.
                bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=6, radius=0.12, enter_editmode=False, align='WORLD', location=(0,X[itr]/X_scale,y[itr]/y_scale))
                # The Name will be in the format : "Scatter No: 0, Cat: Male"
                bpy.context.active_object.name = "Scatter No:" + str(itr) + ", Cat :" + str(categories[i]) 
                # The material will be created and applied.
                createMaterial(
                    materialName="ScatterMaterial :"+str(categories[i]), diffuseColor=scatterMaterial[i][1]
                )
                mesh = bpy.context.object.data
                for f in mesh.polygons:
                    f.use_smooth = True
        
    bpy.ops.object.select_all(action = 'DESELECT')
    return

if __name__ == "__main__":
    # Json parsing.
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    scatterPlot2D(
        X=argv["X"], y=argv["y"], cat=argv["cat"],
        gridMaterial=argv["gridMaterial"], numberMaterial=argv["numberMaterial"]
    )