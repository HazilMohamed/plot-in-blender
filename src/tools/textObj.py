import bpy
import bmesh

from createMaterial import createMaterial

def textObj(text, textType, textPos, textRot, textScale=(0.75,0.75,0.75), numberMaterial=(1,1,1,1)):
    """
    The function creates font objects and convert it into meshes.
    Arguments:
        text            : The text to written in the Viewport.
        textType        : The name to be used in object Collection.
        textPos         : The position of object in the Viewport.
        textRot         : The rotation of object in the Viewport.
        textScale       : The scaling of object in the ViewPort. Default value is (0.75,0.75,0.75).
        numberMaterial  : The material color of numbers. Default value gives White.  
    """
    
    font_curve = bpy.data.curves.new(type="FONT",name="Font Curve")
    font_curve.body = str(text)
    font_obj = bpy.data.objects.new(textType + " " + str(text), font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    bpy.data.objects[textType + " " + str(text)].select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    font_obj.location = textPos
    font_obj.rotation_euler = textRot
    font_obj.scale = textScale
    bpy.context.view_layer.objects.active = font_obj
    bpy.context.active_object.select_set(True)
    bpy.ops.object.convert(target="MESH")
    createMaterial("NumberMaterial",numberMaterial)
    return