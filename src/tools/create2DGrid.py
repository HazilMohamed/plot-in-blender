import bpy
import bmesh

from createMaterial import createMaterial

def create2DGrid(gridName, gridSize, gridLoc, gridRot, x_sub, y_sub, gridMaterial=(1,1,1,1)):
    bpy.ops.mesh.primitive_grid_add(size=gridSize, location=gridLoc, rotation=gridRot, x_subdivisions=x_sub, y_subdivisions=y_sub)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.context.active_object.name = "Grid " + gridName
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None

    #changing origin to origin of plot
    for v in bm.verts:
        if v.index == 0:
            v.select = True
            co = v.co
            bpy.context.scene.cursor.location = (co.x,co.y,co.z)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            break
    if co.y == co.z:
        bpy.ops.transform.translate(value=(0, 0-co.y, 0-co.z), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    elif co.x == co.y:
        bpy.ops.transform.translate(value=(0-co.x, 0-co.y, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    elif co.x == co.z:
        bpy.ops.transform.translate(value=(0-co.x, 0, 0-co.z), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    
    #adding wireframe modifier
    bpy.ops.object.modifier_add(type='WIREFRAME')
    bpy.context.object.modifiers["Wireframe"].thickness = 0.05
    createMaterial("GridMaterial", gridMaterial)
    return