import bpy
import bmesh

from createMaterial import createMaterial

def textObj(text, textType, textPos, textRot, textScale=(0.75,0.75,0.75), numberMaterial=(1,1,1,1)):
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