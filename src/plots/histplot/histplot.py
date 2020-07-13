import bpy
import bmesh
import math
import sys
import json

sys.path.append("src/classes/common_tools")

from common_tools import CommonTools

class HistPlot(CommonTools):
    """
    ========
    HISTPLOT
    ========
    A histplot is a graphical representation that organizes
    a group of data points into user-specified ranges.
    Inheritted Class:
        CommonTools         : It consists of basic operations needed for plotting.
    Arguments :
        x                   : The array of values passed by user. It must be of number data type.
        grid_material       : The material color for grid in plot. Default color is White.
        number_material     : The material color for numbers in plot. Default color is White.
        bins                : The class interval for blocking the data values.
        cat                 : The array of categorical values respected to each value in array x.  
    Methods:
        histplot            : The main function to plot.
    """
    def __init__(
            self, x, grid_material, 
            number_material, bins=None, cat=None):
        self.x = x
        self.grid_material = grid_material
        self.number_material = number_material
        self.bins = bins
        self.cat = cat
        self.bar_material = [
            ("red",(1,0,0,1)), ("yellow",(1,1,0,1)), ("blue",(0,0,1,1)),
            ("green",(0,1,0,1)), ("cyan",(0,1,1,1)), ("purple",(1,0,1,1)),
            ("magenda",(1,0,0.25,1), ("orange",(1,0.25,0,1)))
        ]
    
    def histplot(self):
        # Delete everything on the screen.
        self.clear_screen()

        # Variables used in the function.
        x_cat = []
        x_cat.extend([list(a) for a in zip(self.x, self.cat)])
        x_cat.sort(key=lambda x: x[0])
        max_val = x_cat[-1][0]
        min_val = x_cat[0][0]
        if self.bins is None:
            values = math.ceil(math.sqrt(len(x_cat)))
            self.bins = math.ceil((max_val-min_val)/values)
        size_bar = 1
        y_cat = []
        y_cursor = size_bar/2
        x_new = list(range(math.ceil(min_val-1),math.ceil(max_val),self.bins))
        categories = list(set(self.cat))
        y_cursor = size_bar/2

        # Divide and calculate the heights of plots respect to bins.
        for category in categories:
            y_new = []
            hist = 0
            current = self.bins
            count = 0
            while count < len(x_cat):
                if x_cat[count][0] <= current:
                    if x_cat[count][1] == category:
                        hist += 1
                    count += 1
                else:
                    y_new.append(hist)
                    current += self.bins
                    hist = 0
            y_new.append(hist)
            y_cat.append(y_new)
        y_scale = math.ceil(max_val/10)
        x_scale = 10/len(x_new)

        # Switching to material mode.
        self.change_viewport(shading="MATERIAL")

        # 0.01 is added in the Location is to prevent face mix.
        self.create_2D_grid(
            grid_name="x-Y", grid_size=10, grid_pos=(-(size_bar/2)+0.01, 0, 0),
            grid_rot=(math.radians(0), math.radians(-90), math.radians(0)),
            x_sub=11, y_sub=2, grid_material=self.grid_material)

        # Y axis will be numbered.
        for num in range(11):    
            self.text_obj(
                text=num*y_scale, text_type="y_plot", text_pos=(-(size_bar/2), -1, num),
                text_rot=(math.radians(90),math.radians(0) ,math.radians(90)),
                number_material=self.number_material)        

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
                self.create_material(
                    material_name="BarMaterial "+ str(categories[i]), diffuse_color=self.bar_material[i][1])
            
                # Scaling bar plots in x axis.
                self.transform(
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
            self.text_obj(
                text=x_new[itr], text_type="X_plot", text_pos=(0, x_scale*itr, -1),
                text_rot=(math.radians(90),math.radians(0),math.radians(90)),
                text_scale=(min(1,x_scale/1.5), min(1,x_scale/1.5), min(1,x_scale/1.5)),
                number_material=self.number_material) 

        # To plot the last number of x axis
        self.text_obj(
            text=max(x_new)+self.bins, text_type="X_plot", text_pos=(0, 10, -1),
            text_rot=(math.radians(90),math.radians(0),math.radians(90)),
            text_scale=(min(1,x_scale/1.5), min(1,x_scale/1.5), min(1,x_scale/1.5)), 
            number_material=self.number_material)    
        bpy.ops.object.select_all(action = 'DESELECT')
        return

if __name__ == "__main__":
    # Json parsing. 
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    plot = HistPlot(
        x=argv["x"], bins=argv["bins"], cat=argv["cat"],
        grid_material=argv["grid_material"], number_material=argv["number_material"])
    plot.histplot()