import bpy
import bmesh
import math
import sys
import json

sys.path.append("src/tools/")

from create2Dgrid import create2Dgrid
from textobj import textobj
from transform import transform
from clearscreen import clearscreen
from creatematerial import creatematerial

def barplot(x, y, grid_material, bar_material, number_material):
    """
    =======
    BARPLOT
    =======
    A barplot shows the relationship between a numeric and a categoric variable. 
    Each entity of the categoric variable is represented as a bar. 
    The size of the bar represents its numeric value. 
    Arguments :
        x               : The array of values passed by user. It must be of number data type.
        y               : The array of categoric values respected to x array.
        grid_material    : The material color for grid in plot. Default color is White.
        number_material  : The material color for numbers in plot. Default color is White.
        bar_material     : The material color for bars in plot. Default color is Red.
    Imported User Defined Functions :
        clearscreen     : It will delete everything on the Blender Viewport .
        textobj         : It will create a text object and convert into meshes.
        transform       : This will be used as move function for objects.
        creatematerial  : The materials were created and assigned if not exist.
    """
    # Delete everything on the screen.
    clearscreen()
    
    # Variables used in the function.
    max_val = max(y)
    total = len(x)
    x_scale = 10/total
    y_scale = math.ceil(max_val/10)
    size_bar = 1
    cursor = size_bar/2

    # 0.01 is added in the Location is to prevent face mix.
    create2Dgrid(
        grid_name="X_Y",grid_size=10,grid_pos=(-(size_bar/2)+0.01, 0, 0), 
        grid_rot=(math.radians(0), math.radians(-90), math.radians(0)), 
        x_sub=11, y_sub=2, grid_material=grid_material)

    # Y axis will be numbered.
    for num in range(11):    
        textobj(
            text=num*y_scale, text_type="y_plot", text_pos=(-(size_bar/2), -1, num), 
            text_rot=(math.radians(90),math.radians(0) ,math.radians(90)), 
            number_material=number_material)

    # x axis will be numbered and graph will be plotted.
    for itr in range(total):
        # Create a plane and extruded to a bar.
        bpy.ops.mesh.primitive_plane_add(
            size=size_bar, enter_editmode=False, location=(0, cursor, 0))
        bpy.context.active_object.name = "Bar "+str(x[itr])
        # The material will be created and applied.
        creatematerial(
            material_name="BarMaterial",
            diffuse_color=bar_material
        )

        # Scaling bar plots in x axis.
        transform(
            mode='EDIT',type='EDGE',size_bar=size_bar, 
            x_scale=x_scale, indices=[2,3]) #[2,3] reps rhs of plane from user perspective
        
        # Extruding plane in Z-axis to make into bar.
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type = 'FACE')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, y[itr]/y_scale)})
        bpy.ops.object.mode_set( mode = 'OBJECT' )
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        bpy.ops.object.select_all(action = 'DESELECT')
        textobj(
            text=x[itr], text_type="X_plot", text_pos=(0, (x_scale-size_bar)/2+cursor, -1), 
            text_rot=(math.radians(90),math.radians(90),math.radians(90)),
            text_scale=(min(1,x_scale), min(1,x_scale), min(1,x_scale)), number_material=number_material,
            change_origin=False)
        first_origin = bpy.context.object.matrix_world.to_translation()
        bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        second_origin = bpy.context.object.matrix_world.to_translation()
        bpy.ops.transform.translate(
            value=(0, (first_origin.y - second_origin.y), 0), orient_type='GLOBAL', 
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        cursor += x_scale

    bpy.ops.object.select_all(action = 'DESELECT')
    return


if __name__ == "__main__":
    #Json parsing
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    barplot(
        x=argv["x"], y=argv["y"],
        grid_material=argv["grid_material"], bar_material=argv["bar_material"],
        number_material=argv["number_material"])