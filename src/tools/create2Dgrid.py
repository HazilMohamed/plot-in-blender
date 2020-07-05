import bpy
import bmesh

from creatematerial import creatematerial

def create2Dgrid(
        grid_name, grid_size, grid_pos, grid_rot, 
        x_sub, y_sub, grid_material=(1,1,1,1)):
    """
    Create a Grid of provided size. It will be of square of size provided in grid_size.
    Arguments:
        grid_name        : The name of grid.
        grid_size        : The size of grid.
        grid_pos         : The global position of grid.
        x_sub           : The subdivisions in x axis.
        y_sub           : The subdivisions in y axis.
        grid_material    : The material color of grid. Default value gives White diffuse material
    Imported User Defined Functions :
        creatematerial  : The materials were created and assigned if not exist.
    """

    bpy.ops.mesh.primitive_grid_add(
        size=grid_size, location=grid_pos, rotation=grid_rot, 
        x_subdivisions=x_sub, y_subdivisions=y_sub)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.context.active_object.name = "Grid " + grid_name
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None

    # Changing origin to origin of plot.
    for v in bm.verts:
        if v.index == 0:
            v.select = True
            co = v.co
            bpy.context.scene.cursor.location = (co.x,co.y,co.z)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            break
    if co.y == co.z:
        bpy.ops.transform.translate(
            value=(0, 0-co.y, 0-co.z), orient_type='GLOBAL', 
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    elif co.x == co.y:
        bpy.ops.transform.translate(
            value=(0-co.x, 0-co.y, 0), orient_type='GLOBAL', 
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    elif co.x == co.z:
        bpy.ops.transform.translate(
            value=(0-co.x, 0, 0-co.z), orient_type='GLOBAL', 
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    
    # Adding wireframe modifier to get grid structure.
    bpy.ops.object.modifier_add(type='WIREFRAME')
    bpy.context.object.modifiers["Wireframe"].thickness = 0.05
    creatematerial("GridMaterial", grid_material)
    return