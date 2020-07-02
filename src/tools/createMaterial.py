import bpy

def createMaterial(materialName,diffuseColor):
    """
    The function creates a material if that materialName doesn't exist, 
    use the material to that object if it's already exists. 
    Arguments:
        materialName    : The name of material to be used.
        diffuseColor    : The (R,G,B,A) value to be given for diffuse material.
    """
    
    mat = bpy.data.materials.get(materialName)
    if mat is None:
        mat = bpy.data.materials.new(materialName)
    activeObject = bpy.context.active_object 
    activeObject.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = diffuseColor
    return