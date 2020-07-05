import bpy
import bmesh

def transform(mode, type, size_bar, x_scale, indices):
    """
    The function is used to scale the bars in BarCharts to appropraite size.
    Arguments:
        mode        : To select the mode.
        type        : To select type of editing. Available values are [VERT, EDGE, FACE].
        size_bar    : Gives the size of bar to be transformed.
        x_scale     : Gives the scale factor to adjsuted.
        indices     : List of vertices needs to selected for scaling.
    """
    
    bpy.ops.object.mode_set(mode = mode)
    bpy.ops.mesh.select_mode(type = type)
    bpy.ops.mesh.select_all(action = 'DESELECT')
    me = bpy.context.active_object.data
    bm = bmesh.from_edit_mesh(me)
    for edge in bm.edges:
        if edge.verts[0].index in indices and edge.verts[1].index in indices:
            edge.select = True
            bpy.ops.transform.translate(
                value=(0, (x_scale-size_bar), 0), 
                orient_type='GLOBAL', 
                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
            break
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    return