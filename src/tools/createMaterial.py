import bpy

def createMaterial(materialName,diffuseColor):
    mat = bpy.data.materials.get(materialName)
    if mat is None:
        mat = bpy.data.materials.new(materialName)
    activeObject = bpy.context.active_object 
    activeObject.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = diffuseColor
    return