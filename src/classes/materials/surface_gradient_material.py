import bpy
import random

from principle_material import PrincipleMaterial

class SurfaceGradientMaterial():
    """
    =========================
    SURFACE GRADIENT MATERIAL
    =========================
    The class is used to create a gradient shader w.r.t to z axis is created.
    Imported Class:
        PrincipleMaterial           : Used to create Principle BSDF.
    Methods:
        create_gradient             : Used to create gradient.
        create_surface_material     : Used to create gradient shader. 
    """
    def __init__(self, gradient_name):
        self.gradient_name = gradient_name
        self.variants_and_gradients = {
            "flames": [
                (1.000, 0.909, 0.031, 1), (1.000, 0.808, 0.000, 1), (1.000, 0.604, 0.000, 1),
                (1.000, 0.352, 0.000, 1), (1.000, 0.000, 0.000, 1)
            ],
            "ocean": [
                (0.964, 0.976, 1.000, 1), (0.847, 0.867, 1.000, 1), (0.364, 0.533, 0.816, 1),
                (0.208, 0.216, 0.721, 1), (0.098, 0.157, 0.455, 1)
            ],
            "sunset": [
                (0.980, 0.757, 0.541, 1), (0.945, 0.506, 0.372, 1), (0.674, 0.345, 0.380, 1),
                (0.384, 0.207, 0.309, 1), (0.176, 0.157, 0.294, 1)
            ],
            "forest": [
                (0.643, 0.984, 0.651, 1), (0.290, 0.898, 0.290,  1), (0.188, 0.796, 0.000, 1),
                (0.059, 0.572, 0.000, 1), (0.000, 0.384, 0.012, 1)
            ]
        }
        pass

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
            elements[idx].color = section
            elements[idx].position = position
            position += (20 / 100.0) 

    def create_surface_material(self):
        material = bpy.data.materials.get("Surface Gradient Material")
        if material is None:
            material = bpy.data.materials.new(name="Surface Gradient Material")

        material.use_nodes = True
        mats = bpy.data.materials
        nodes = mats['Surface Gradient Material'].node_tree.nodes
        
        color_ramp = nodes.get("ColorRamp")
        if color_ramp is not None:
            nodes.remove(color_ramp)
        color_ramp = material.node_tree.nodes.new("ShaderNodeValToRGB")
        elements = nodes["ColorRamp"].color_ramp.elements
        nodes["ColorRamp"].color_ramp.interpolation = "EASE"
        
        print(self.variants_and_gradients.get(self.gradient_name))
        self.create_gradient(elements, self.variants_and_gradients.get(self.gradient_name))
            
        principled_bsdf = nodes.get("Principled BSDF")
        material.node_tree.links.new(principled_bsdf.inputs["Base Color"], color_ramp.outputs["Color"])

        separate_xyz = nodes.get("Separate XYZ")
        if separate_xyz is not None:
            nodes.remove(separate_xyz)
        separate_xyz = material.node_tree.nodes.new("ShaderNodeSeparateXYZ")
        material.node_tree.links.new(color_ramp.inputs["Fac"], separate_xyz.outputs["Z"])

        texture_cord = nodes.get("Texture Coordinate")
        if texture_cord is not None:
            nodes.remove(texture_cord)
        texture_cord = material.node_tree.nodes.new("ShaderNodeTexCoord")
        material.node_tree.links.new(separate_xyz.inputs["Vector"], texture_cord.outputs["Generated"])
        return material