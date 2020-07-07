import bpy
import bmesh

from creatematerial import creatematerial

def textobj(
        text, text_type, text_pos, text_rot, 
        text_scale=(0.75,0.75,0.75), number_material=(1,1,1,1),
        change_origin=True):
    """
    The function creates font objects and convert it into meshes.
    Arguments:
        text                : The text to written in the Viewport.
        text_type           : The name to be used in object Collection.
        text_pos            : The position of object in the Viewport.
        text_rot            : The rotation of object in the Viewport.
        text_scale          : The scaling of object in the ViewPort. Default value is (0.75,0.75,0.75).
        number_material     : The material color of numbers. Default value gives White.  
        change_origin       : Changes the origin to center of mass of Object.
    """
    
    font_curve = bpy.data.curves.new(type="FONT",name="Font Curve")
    font_curve.body = str(text)
    font_obj = bpy.data.objects.new(text_type + " " + str(text), font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    bpy.data.objects[text_type + " " + str(text)].select_set(True)
    if change_origin == True:
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    font_obj.location = text_pos
    font_obj.rotation_euler = text_rot
    font_obj.scale = text_scale
    bpy.context.view_layer.objects.active = font_obj
    bpy.context.active_object.select_set(True)
    bpy.ops.object.convert(target="MESH")
    creatematerial("NumberMaterial",number_material)
    return