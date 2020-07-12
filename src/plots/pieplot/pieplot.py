import bpy
import random
import sys
import json

sys.path.append("src/tools/")

from clearscreen import clearscreen
from createpiematerial import PieMaterial

# Create a material that uses nodes
def pieplot(x, y):
    """
    =======
    PIEPLOT
    =======
    A pieplot (or a pie chart) is a circular statistical graphic, 
    which is divided into slices to illustrate numerical proportion.
    Arguments :
        x   : The array of numerical values.
        y   : The array of categorical values respected to x array.
    Imported User Defined Functions and Classes :
        PieMaterial     : The class used to create shader node for plotting.
        clearscreen     : It will delete everything on the Blender Viewport.
    """

    # Delete everything on the screen.
    clearscreen()

    # Switching to material mode.
    my_areas = bpy.context.workspace.screens[0].areas
    my_shading = 'MATERIAL'  
    for area in my_areas:
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = my_shading

    # Variables used in the function.
    percent_of_x = []
    for i in x:
        percent_of_x.append(i*100/sum(x))

    # Instanciating class "PieMaterial".
    material = PieMaterial(percent_of_x)
    
    # Creating a cylinder for pie plot.
    bpy.ops.mesh.primitive_cylinder_add(
        radius=5, depth=0.7, enter_editmode=False, 
        align='WORLD', location=(0, 0, 0))
    active_object = bpy.context.active_object
    active_object.name = "Pie Plot"
    active_object.data.materials.append(material.create_pie_material())

    bpy.ops.object.select_all(action = 'DESELECT')
    return

if __name__ == "__main__":
    # Json parsing
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    pieplot(
        x=argv["x"], y=argv["y"])