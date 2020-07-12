import bpy

def change_viewport(shading="SOLID"):
    """
    The function uses change the shading of viewport.
    Arguments:
        shading     : accepts already declared values from enum  [SOLID, WIREFRAME, MATERIAL, RENDERED].
    """
    my_areas = bpy.context.workspace.screens[0].areas
    my_shading = shading  
    for area in my_areas:
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = my_shading
    return