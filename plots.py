import bpy
import math
import bmesh
import sys
import json

#available plots go here
plots = ["barPlot"]

def init():
    
    #deleting previous
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()

    #json data values
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])
   
    eval(argv["plotName"])(argv["X"],argv["y"])  
    
#function to create text objects       
def textObj(text, textType, textPos, textRot, textScale=(0.75,0.75,0.75)):
    font_curve = bpy.data.curves.new(type="FONT",name="Font Curve")
    font_curve.body = str(text)
    font_obj = bpy.data.objects.new(textType + " " + str(text), font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    bpy.data.objects[textType + " " + str(text)].select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    font_obj.location = textPos
    font_obj.rotation_euler = textRot
    font_obj.scale = textScale
    return
 
#function to create move meshes   
def transform(mode, type, size_bar, X_scale, indices):
    bpy.ops.object.mode_set(mode = mode)
    bpy.ops.mesh.select_mode(type = type)
    bpy.ops.mesh.select_all(action = 'DESELECT')
    me = bpy.context.active_object.data
    bm = bmesh.from_edit_mesh(me)
    for edge in bm.edges:
        if edge.verts[0].index in indices and edge.verts[1].index in indices:
            edge.select = True
            bpy.ops.transform.translate(value=(0, (X_scale-size_bar), 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
            break
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    return
    

def barPlot(X,y):
    #local variables
    maxVal = max(y)
    total = len(X)
    X_scale = 11/total
    y_scale = math.ceil(maxVal/10)
    size_bar = 1
    cursor = size_bar/2

    #adding grid 0.01 is used to push grid little back else face mix will happen
    bpy.ops.mesh.primitive_grid_add(size=11, location=(-(size_bar/2)+0.01, 0, 0), rotation=(math.radians(0), math.radians(-90), math.radians(0)), x_subdivisions=12, y_subdivisions=2)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
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
    bpy.ops.transform.translate(value=(0, 0-co.y, 0-co.z), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))

    #numbering y-axis
    for num in range(11):    
        textObj(num*y_scale, "y_plot", (-(size_bar/2), -1, num), (math.radians(90),math.radians(0) ,math.radians(90)))

    #plotting and naming x axis
    for itr in range(total):
        #initilializing a plane
        bpy.ops.mesh.primitive_plane_add(size=size_bar, enter_editmode=False, location=(0, cursor, 0))
        bpy.context.active_object.name = "Bar "+str(X[itr])
        
        #scaling bar plots
        transform('EDIT', 'EDGE', size_bar, X_scale, [2,3]) #[2,3] reps rhs of plane from user perspective
        
        #extruding plane along z axis
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type = 'FACE')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, y[itr]/y_scale)}
        )
        bpy.ops.object.mode_set( mode = 'OBJECT' )
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        textObj(X[itr], "X_plot", (0, (X_scale-size_bar)/2+cursor, -1), (math.radians(90),math.radians(90),math.radians(90)),(min(1,X_scale), min(1,X_scale), min(1,X_scale))) 
        cursor += X_scale

    bpy.ops.object.select_all(action = 'DESELECT')
        
if __name__ == "__main__":
    init()
