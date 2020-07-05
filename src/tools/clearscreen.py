import bpy

def clearscreen():
    """
    Delete everything from 3D viewport of Blender. 
    """
    
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()
    return