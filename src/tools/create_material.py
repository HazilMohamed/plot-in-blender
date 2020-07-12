import bpy

def create_material(material_name,diffuse_color):
    """
    The function creates a material if that material_name doesn't exist, 
    use the material to that object if it's already exists. 
    Arguments:
        material_name    : The name of material to be used.
        diffuse_color    : The (R,G,B,A) value to be given for diffuse material.
    """
    
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        mat = bpy.data.materials.new(material_name)
    activeObject = bpy.context.active_object 
    activeObject.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = diffuse_color
    return