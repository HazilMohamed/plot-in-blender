import bpy
import random

class PrincipleMaterial():
    """
    ==================
    PRINCIPLE MATERIAL
    ==================
    The function creates a material a basic principle BSDF if that material_name doesn't exist, 
    use the material to that object if it's already exists. 
    Arguments:
        material_name           : The name of material to be used.
        diffuse_color           : The (R,G,B,A) value to be given for diffuse material.
    Methods:
        create_principle_bsdf   : The main function create material.
        generate_random_color   : A random color is generated if not color is given.
    """ 
    def __init__(self, material_name, material_color=None):
        self.material_name = material_name
        if material_color is None:
            self.material_color = self.generate_random_color()
        else:
            self.material_color = material_color

    def generate_random_color(self):
        RAN = random.random
        return ((RAN(), RAN(), RAN(), 1))
    
    def create_principle_bsdf(self):
        material = bpy.data.materials.get(self.material_name)
        if material is None:
            material = bpy.data.materials.new(self.material_name)
        material.use_nodes = True
        mats = bpy.data.materials
        nodes = mats[self.material_name].node_tree.nodes

        principled_bsdf = nodes.get("Principled BSDF")
        if principled_bsdf is None:
            nodes.remove(principled_bsdf)
        principled_bsdf.inputs["Base Color"].default_value = self.material_color
        return material