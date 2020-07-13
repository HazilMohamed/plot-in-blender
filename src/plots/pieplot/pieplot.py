import bpy
import random
import sys
import json

sys.path.append("src/tools/")

from clear_screen import clear_screen
from change_viewport import change_viewport

class PieMaterial():
    """
    -----------
    PIEMATERIAL
    -----------
    The class is used to create gradient used in pieplots.
    
    Methods:
        create_values_and_colors    : This will form nested list of [value,color_code].
        get_random_color            : Used to create random colors.
        create_pie_material         : Used to create shader of pieplot.
        create_gradient             : This sections adds or removes elements if you update your procents_and_colors list with more / fewer elements
    """
    def __init__(self, percent_of_x):
        self.values_and_colors = []
        self.percent_of_x = percent_of_x 
    
    def create_values_and_colors(self):
        for i in self.percent_of_x:
            self.values_and_colors.append([i,self.get_random_color()])
        return self.values_and_colors

    def get_random_color(self):
        RAN = random.random
        return ((RAN(), RAN(), RAN(), 1.0))

    def create_gradient(self, elements, procents_and_colors):
        diff = len(elements) - len(procents_and_colors)
        if diff > 0:
            for _ in range(abs(diff)):
                elements.remove(elements[-1])
        elif diff < 0:
            for _ in range(abs(diff)):
                elements.new(position=0.0)
            
        position = 0
        for idx, section in enumerate(procents_and_colors):
            elements[idx].color = section[1]
            elements[idx].position = position
            position += (section[0] / 100.0)        
      
    def create_pie_material(self):
        material = bpy.data.materials.get("Pie Plot")
        if material is None:
            material = bpy.data.materials.new(name="Pie Plot")

        material.use_nodes = True
        mats = bpy.data.materials
        nodes = mats['Pie Plot'].node_tree.nodes
        color_ramp = nodes.get("ColorRamp")

        if color_ramp is not None:
            nodes.remove(color_ramp)
        color_ramp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        elements = nodes["ColorRamp"].color_ramp.elements
        nodes["ColorRamp"].color_ramp.interpolation = "CONSTANT"
        
        procents_and_colors = self.create_values_and_colors()

        self.create_gradient(elements, procents_and_colors)
            
        principled_bsdf = nodes.get("Principled BSDF")
        material.node_tree.links.new(principled_bsdf.inputs["Base Color"], color_ramp.outputs["Color"])

        gradient = nodes.get("Gradient Texture")
        if gradient is not None:
            nodes.remove(gradient)
        gradient = material.node_tree.nodes.new("ShaderNodeTexGradient")
        gradient.gradient_type = "RADIAL"
        material.node_tree.links.new(color_ramp.inputs["Fac"], gradient.outputs["Color"])

        texture_cord = nodes.get("Texture Coordinate")
        if texture_cord is not None:
            nodes.remove(texture_cord)
        texture_cord = material.node_tree.nodes.new("ShaderNodeTexCoord")
        material.node_tree.links.new(gradient.inputs["Vector"], texture_cord.outputs["Object"])
        return material


# Create a material that uses nodes
def pieplot(x, y):
    """
    =======
    PIEPLOT
    =======
    A pieplot (or a pie chart) is a circular statistical graphic, 
    which is divided into slices to illustrate numerical proportion.
    Arguments :
        x                   : The array of numerical values.
        y                   : The array of categorical values respected to x array.
    Imported User Defined Functions and Classes :
        PieMaterial         : The class used to create shader node for plotting.
        clear_screen        : It will delete everything on the Blender Viewport.
        change_viewport     : Changes mode of viewport.
    """

    # Delete everything on the screen.
    clear_screen()

    # Switching to material mode.
    change_viewport(shading="MATERIAL")

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