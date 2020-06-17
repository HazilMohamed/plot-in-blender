import bpy

def clearScreen():
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()