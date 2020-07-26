import bpy
import bmesh
import math
import sys
import json
import random

sys.path.append("src/classes/common_tools")
sys.path.append("src/classes/materials")

from common_tools import CommonTools
from principle_material import PrincipleMaterial

class CountPlot(CommonTools):
    """
    =======
    COUNTPLOT
    =======
    A countplot shows the counts of observations in each categorical bin using bars.
    Each entity of the categoric variable is represented as a bar. 
    The size of the bar represents its count.
    Inheritted Class:
        CommonTools         : It consists of basic operations needed for plotting. 
    Imported Class:
        PrincipleMaterial   : Used to create principle material.
    Arguments :
        x                   : The array of values passed by user. It must be of number data type.
        grid_material       : The material color for grid in plot. Default color is White.
        number_material     : The material color for numbers in plot. Default color is White.
    Methods:
        countplot           : The main function to plot.
        generate_color     : Generate random colors for each categories.
    """
    def __init__(
            self, x, cat,  
            grid_material, number_material):
        self.x = x
        self.cat = cat
        self.grid_material = grid_material
        self.number_material = number_material
        self.counter = {}
        self.color_list = []

    def generate_color(self):
        RAN = random.random
        return ((RAN(), RAN(), RAN(), 1.0))

    def countplot(self):
        # Delete everything on the screen.
        self.clear_screen()
        
        # Variables used in the function.
        for i in range(len(self.x)):
            if self.x[i] not in self.counter.keys():
                self.counter[self.x[i]] = {}
            if self.cat[i] not in self.counter[self.x[i]].keys():
                self.counter[self.x[i]][self.cat[i]] = 1
            else:
                self.counter[self.x[i]][self.cat[i]] += 1

        for i in self.counter:
            j = dict(sorted(self.counter[i].items()))
            self.counter[i] = j

        cat_set = set(self.cat)
        for item in self.counter:
            for cat in cat_set:
                if cat not in self.counter[item].keys():
                    self.counter[item][cat] = 0
        
        for cat in cat_set:
            self.color_list.append(self.generate_color())

        self.counter = dict(sorted(self.counter.items()))
        max_val = max(max(self.counter[item].values()) for item in self.counter)
        x_scale = 10/(max(len(self.counter[item]) for item in self.counter)*len(self.counter.items()))
        
        y_scale = math.ceil(max_val/10)
        size_bar = 1
        cursor = size_bar/2
        
        # Switching to material mode.
        self.change_viewport(shading="MATERIAL")

        # # 0.01 is added in the Location is to prevent face mix.
        self.create_2D_grid(
            grid_name="X_Y",grid_size=10,grid_pos=(-(size_bar/2)+0.01, 0, 0), 
            grid_rot=(math.radians(0), math.radians(-90), math.radians(0)), 
            x_sub=11, y_sub=2, grid_material=self.grid_material)

        # # Y axis will be numbered.
        for num in range(11):    
            self.text_obj(
                text=num*y_scale, text_type="y_plot", text_pos=(-(size_bar/2), -1, num), 
                text_rot=(math.radians(90),math.radians(0) ,math.radians(90)), 
                number_material=self.number_material)

        # # x axis will be numbered and graph will be plotted.
        for itr in self.counter:
            color = 0
            self.text_obj(
                    text=itr, text_type="X_plot", text_pos=(0, (len(cat_set)*x_scale-size_bar)/2+cursor, -1), 
                    text_rot=(math.radians(90),math.radians(90),math.radians(90)),
                    text_scale=(min(1,x_scale), min(1,x_scale), min(1,x_scale)),
                    number_material=self.number_material, change_origin=False)
            
            for cat in self.counter[itr]:
                if self.counter[itr][cat] == 0:
                    cursor += x_scale
                    continue
                
                # Create a plane and extruded to a bar.
                bpy.ops.mesh.primitive_plane_add(
                    size=size_bar, enter_editmode=False, location=(0, cursor, 0))
                bpy.context.active_object.name = "Bar "+str(itr)+" "+str(cat)
                
                # The material will be created and applied.
                activeObject = bpy.context.active_object
                material = PrincipleMaterial(
                                "BarMaterial "+str(itr)+" "+str(cat), self.color_list[color]) 
                activeObject.data.materials.append(material.create_principle_bsdf())

                # Scaling bar plots in x axis.
                self.transform(
                    mode='EDIT',type='EDGE',size_bar=size_bar, 
                    x_scale=x_scale, indices=[2,3]) #[2,3] reps rhs of plane from user perspective
                
                # Extruding plane in Z-axis to make into bar.
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_mode(type = 'FACE')
                bpy.ops.mesh.select_all(action = 'SELECT')
                bpy.ops.mesh.extrude_region_move(
                    TRANSFORM_OT_translate={"value":(0, 0, self.counter[itr][cat]/y_scale)})
                bpy.ops.object.mode_set( mode = 'OBJECT' )
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
                bpy.ops.object.select_all(action = 'DESELECT')
                
                first_origin = bpy.context.object.matrix_world.to_translation()
                bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_MASS', center='MEDIAN')
                second_origin = bpy.context.object.matrix_world.to_translation()
                bpy.ops.transform.translate(
                    value=(0, (first_origin.y - second_origin.y), 0), orient_type='GLOBAL', 
                    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
                cursor += x_scale
                color += 1
    
            bpy.ops.object.select_all(action = 'DESELECT')
        return

if __name__ == "__main__":
    # Json parsing
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    plot = CountPlot(
        x=argv["x"], cat=argv["cat"],
        grid_material=argv["grid_material"], number_material=argv["number_material"])
    plot.countplot()