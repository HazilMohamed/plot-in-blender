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
    #To delete default objects
    clearScreen()
    
    #local variables
    X_maxVal = max(X)
    y_maxVal = max(y)
    z_maxVal = max(z)
    X_scale = math.ceil(X_maxVal/10)
    y_scale = math.ceil(y_maxVal/10)
    z_scale = math.ceil(z_maxVal/10)
    total = len(X)

    #adding 3D grid
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
    #numbering X-axis, y-axis and z-axis
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
    #plotting
    for itr in range(total):
        #plotting sphere
        bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=6, radius=0.2, enter_editmode=False, align='WORLD', location=(X[itr]/X_scale,y[itr]/y_scale,z[itr]/z_scale))
        bpy.context.active_object.name = "scatter "+str(itr)
        createMaterial(
            materialName="ScatterMaterial",diffuseColor=scatterMaterial
        )
        
    bpy.ops.object.select_all(action = 'DESELECT')
    return

if __name__ == "__main__":
    #Json parsing
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    scatterPlot3D(
        X=argv["X"], y=argv["y"], z=argv["z"],
        gridMaterial=argv["gridMaterial"], scatterMaterial=argv["scatterMaterial"], numberMaterial=argv["numberMaterial"]    
    )