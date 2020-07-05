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

def histplot(x, grid_material, number_material, bins=None, cat=None):
    """
    ========
    HISTPLOT
    ========
    A histplot is a graphical representation that organizes
    a group of data points into user-specified ranges.
    Arguments :
        x               : The array of values passed by user. It must be of number data type.
        grid_material    : The material color for grid in plot. Default color is White.
        number_material  : The material color for numbers in plot. Default color is White.
        bins            : The class interval for blocking the data values.
        cat             : The array of categorical values respected to each value in array x.  
    Imported User Defined Functions :
        clearscreen     : It will delete everything on the Blender Viewport .
        textobj         : It will create a text object and convert into meshes.
        transform       : This will be used as move function for objects.
        creatematerial  : The materials were created and assigned if not exist.
    """

    # 8 colors are declared right now for to use, every material is diffuse material in Blender
    bar_material = [
        ("red",(1,0,0,1)), ("yellow",(1,1,0,1)), ("blue",(0,0,1,1)),
        ("green",(0,1,0,1)), ("cyan",(0,1,1,1)), ("purple",(1,0,1,1)),
        ("magenda",(1,0,0.25,1), ("orange",(1,0.25,0,1)))
    ]

    # Delete everything on the screen.
    clearscreen()

    # Variables used in the function.
    x_cat = []
    x_cat.extend([list(a) for a in zip(x, cat)])
    x_cat.sort(key=lambda x: x[0])
    max_val = x_cat[-1][0]
    min_val = x_cat[0][0]
    if bins is None:
        values = math.ceil(math.sqrt(len(x_cat)))
        bins = math.ceil((max_val-min_val)/values)
    y_new = []
    size_bar = 1
    y_cat = []
    y_cursor = size_bar/2
    x_new = list(range(math.ceil(min_val-1),math.ceil(max_val),bins))
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
        while count < len(x_cat):
            if x_cat[count][0] <= current:
                if x_cat[count][1] == category:
                    hist += 1
                count += 1
            else:
                y_new.append(hist)
                current += bins
                hist = 0
        y_new.append(hist)
        y_cat.append(y_new)
    y_scale = math.ceil(max_val/10)
    x_scale = 10/len(x_new)

    # 0.01 is added in the Location is to prevent face mix.
    create2Dgrid(
        grid_name="x-Y", grid_size=10, grid_pos=(-(size_bar/2)+0.01, 0, 0),
        grid_rot=(math.radians(0), math.radians(-90), math.radians(0)),
        x_sub=11, y_sub=2, grid_material=grid_material)

    # Y axis will be numbered.
    for num in range(11):    
        textobj(
            text=num*y_scale, text_type="y_plot", text_pos=(-(size_bar/2), -1, num),
            text_rot=(math.radians(90),math.radians(0) ,math.radians(90)),
            number_material=number_material)        

    # x axis will be numbered and graph will be plotted.
    for itr in range(len(x_new)):
        z_cursor = 0
        for i in range(len(categories)):
            # To check category value exists in the corresponding bins or not.
            if y_cat[i][itr] == 0:
                continue

            # Create a plane and extruded to a bar.
            bpy.ops.mesh.primitive_plane_add(
                size=size_bar, enter_editmode=False, location=(0, y_cursor, z_cursor))
            # The Bar name will be in the format of : "Bar No: 0, Cat: Male, Count: 6"
            bpy.context.active_object.name = "Bar No: " + str(x_new[itr]) + ", Cat: " + str(categories[i]) + ", Count: " + str(y_cat[i][itr])
            # The material will be created and applied.
            creatematerial(
                material_name="BarMaterial "+ str(categories[i]), diffuse_color=bar_material[i][1])
        
            # Scaling bar plots in x axis.
            transform(
                mode='EDIT', type='EDGE', size_bar=size_bar, 
                x_scale=x_scale, indices=[2,3])      #[2,3] represents RHS of plane from user perspective.
        
            # Extruding plane in Z-axis to make into bar.
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_mode(type = 'FACE')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={"value":(0, 0, (y_cat[i][itr]/y_scale))})
            z_cursor += (y_cat[i][itr]/y_scale)
            bpy.ops.object.mode_set( mode = 'OBJECT' )
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        
        y_cursor += x_scale
        textobj(
            text=x_new[itr], text_type="X_plot", text_pos=(0, x_scale*itr, -1),
            text_rot=(math.radians(90),math.radians(0),math.radians(90)),
            text_scale=(min(1,x_scale/1.5), min(1,x_scale/1.5), min(1,x_scale/1.5)),
            number_material=number_material) 

    # To plot the last number of x axis
    textobj(
        text=max(x_new)+bins, text_type="X_plot", text_pos=(0, 10, -1),
        text_rot=(math.radians(90),math.radians(0),math.radians(90)),
        text_scale=(min(1,x_scale/1.5), min(1,x_scale/1.5), min(1,x_scale/1.5)), 
        number_material=number_material)    
    bpy.ops.object.select_all(action = 'DESELECT')
    return

if __name__ == "__main__":
    # Json parsing. 
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    histplot(
        x=argv["x"], bins=argv["bins"], cat=argv["cat"],
        grid_material=argv["grid_material"], number_material=argv["number_material"])