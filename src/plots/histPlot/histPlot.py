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
from createMaterial import createMaterial

def histPlot(X, gridMaterial, numberMaterial, bins=None, cat=None):
    """
    ========
    HISTPLOT
    ========
    A histPlot is a graphical representation that organizes a group of data points into user-specified ranges.
    Arguments :
        X               : The array of values passed by user. It must be of number data type.
        gridMaterial    : The material color for grid in plot. Default color is White.
        numberMaterial  : The material color for numbers in plot. Default color is White.
        bins            : The class interval for blocking the data values. Default value is calculated by the equation [maxVal-minVal]/sqrt(len(X))].
        cat             : The array of categorical values respected to each value in array X.  
    Imported User Defined Functions :
        clearScreen     : It will delete everything on the Blender Viewport .
        textObj         : It will create a text object and convert into meshes.
        transform       : This will be used as move function for objects.
        createMaterial  : The materials were created and assigned if not exist.
    """

    # 8 colors are declared right now for to use, every material is diffuse material in Blender
    barMaterial = [
        ("red",(1,0,0,1)),("yellow",(1,1,0,1)),("blue",(0,0,1,1)),
        ("green",(0,1,0,1)),("cyan",(0,1,1,1)),("purple",(1,0,1,1)),
        ("magenda",(1,0,0.25,1),("orange",(1,0.25,0,1)))
    ]

    # Delete everything on the screen.
    clearScreen()

    # Variables used in the function.
    X_cat = []
    X_cat.extend([list(a) for a in zip(X, cat)])
    X_cat.sort(key=lambda x: x[0])
    maxVal = X_cat[-1][0]
    minVal = X_cat[0][0]
    if bins is None:
        values = math.ceil(math.sqrt(len(X_cat)))
        bins = math.ceil((maxVal-minVal)/values)
    y_new = []
    size_bar = 1
    y_cat = []
    y_cursor = size_bar/2
    X_new = list(range(math.ceil(minVal-1),math.ceil(maxVal),bins))
    current = bins
    categories = list(set(cat))
    y_cursor = size_bar/2

    # Divide and calculate the heights of plots respect to bins.
    for category in categories:
        y_new = []
        hist = 0
        current = bins
        hist = 0
        count = 0
        while count < len(X_cat):
            if X_cat[count][0] <= current:
                if X_cat[count][1] == category:
                    hist += 1
                count += 1
            else:
                y_new.append(hist)
                current += bins
                hist = 0
        y_new.append(hist)
        y_cat.append(y_new)
    y_scale = math.ceil(maxVal/10)
    X_scale = 10/len(X_new)

    # 0.01 is added in the Location is to prevent face mix.
    create2DGrid(
        gridName="X-Y", gridSize=10, gridLoc=(-(size_bar/2)+0.01, 0, 0),
        gridRot=(math.radians(0), math.radians(-90), math.radians(0)),
        x_sub=11, y_sub=2, gridMaterial=gridMaterial
    )

    # Y axis will be numbered.
    for num in range(11):    
        textObj(
            text=num*y_scale, textType="y_plot", 
            textPos=(-(size_bar/2), -1, num), textRot=(math.radians(90),math.radians(0) ,math.radians(90)),
            numberMaterial=numberMaterial
        )        

    # X axis will be numbered and graph will be plotted.
    for itr in range(len(X_new)):
        z_cursor = 0
        for i in range(len(categories)):
            # To check category value exists in the corresponding bins or not.
            if y_cat[i][itr] == 0:
                continue

            # Create a plane and extruded to a bar.
            bpy.ops.mesh.primitive_plane_add(size=size_bar, enter_editmode=False, location=(0, y_cursor, z_cursor))
            # The Bar name will be in the format of : "Bar No: 0, Cat: Male, Count: 6"
            bpy.context.active_object.name = "Bar No: " + str(X_new[itr]) + ", Cat: " + str(categories[i]) + ", Count: " + str(y_cat[i][itr])
            # The material will be created and applied.
            createMaterial(
                materialName="BarMaterial "+ str(categories[i]), diffuseColor=barMaterial[i][1]
            )
        
            # Scaling bar plots in X axis.
            transform(
                mode='EDIT', type='EDGE', size_bar=size_bar, 
                X_scale=X_scale, indices=[2,3]      #[2,3] represents RHS of plane from user perspective.
            )
        
            # Extruding plane in Z-axis to make into bar.
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_mode(type = 'FACE')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={"value":(0, 0, (y_cat[i][itr]/y_scale))}
            )
            z_cursor += (y_cat[i][itr]/y_scale)
            bpy.ops.object.mode_set( mode = 'OBJECT' )
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        y_cursor += X_scale
        textObj(
            text=X_new[itr], textType="X_plot", 
            textPos=(0, X_scale*itr, -1), textRot=(math.radians(90),math.radians(0),math.radians(90)),
            textScale=(min(1,X_scale/1.5), min(1,X_scale/1.5), min(1,X_scale/1.5)),
            numberMaterial=numberMaterial
        ) 
    # To plot the last number of X axis
    textObj(
        text=max(X_new)+bins, textType="X_plot", 
        textPos=(0, 10, -1), textRot=(math.radians(90),math.radians(0),math.radians(90)),
        textScale=(min(1,X_scale/1.5), min(1,X_scale/1.5), min(1,X_scale/1.5)), 
        numberMaterial=numberMaterial
    )    
    bpy.ops.object.select_all(action = 'DESELECT')
    return

if __name__ == "__main__":
    # Json parsing. 
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    histPlot(
        X=argv["X"], bins=argv["bins"], cat=argv["cat"],
        gridMaterial=argv["gridMaterial"],numberMaterial=argv["numberMaterial"]
    )