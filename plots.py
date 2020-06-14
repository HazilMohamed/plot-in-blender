import bpy
import math
import bmesh
import sys
import json

plots2D = ["barPlot","scatterPlot2D"]
plots3D = ["scatterPlot3D"]
 
def init():
    
    #deleting previous
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()

    #json data values
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    if argv["plotName"] in plots2D:
        eval(argv["plotName"])(argv["X"],argv["y"])
    elif argv["plotName"] in plots3D:
        eval(argv["plotName"])(argv["X"],argv["y"],argv["z"])

#function to create 2D grid
def create2DGrid(gridName, gridSize, gridLoc, gridRot, x_sub, y_sub):
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
    return

    
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
    X_scale = 10/total
    y_scale = math.ceil(maxVal/10)
    size_bar = 1
    cursor = size_bar/2

    #adding 2D grid 0.01 is used to push grid little back else face mix will happen
    create2DGrid("X_Y", 10, (-(size_bar/2)+0.01, 0, 0), (math.radians(0), math.radians(-90), math.radians(0)), 11, 2)

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
    
def scatterPlot2D(X,y):
    
    #local variables
    y_maxVal = max(y)
    X_maxVal = max(X)
    X_scale = math.ceil(X_maxVal/10)
    y_scale = math.ceil(y_maxVal/10)
    total = len(X)

    #adding 2D grid
    create2DGrid("X-Y", 10, (0, 0, 0), (math.radians(0), math.radians(-90), math.radians(0)), 11, 11)

    #numbering y-axis and X-axis
    for num in range(11):    
        textObj(int(num*y_scale), "y_plot", (0, -1, num), (math.radians(90),math.radians(0) ,math.radians(90)),textScale=(0.4,0.4,0.4))
        textObj(int(num*X_scale), "X_plot", (0, num, -1), (math.radians(90),math.radians(0),math.radians(90)),textScale=(0.4,0.4,0.4)) 

    #plotting
    for itr in range(total):
        #plotting sphere
        bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=6, radius=0.2, enter_editmode=False, align='WORLD', location=(0,X[itr]/X_scale,y[itr]/y_scale))

        bpy.context.active_object.name = "scatter "+str(itr)
        
    bpy.ops.object.select_all(action = 'DESELECT')

def scatterPlot3D(X,y,z):
    
    #local variables
    X_maxVal = max(X)
    y_maxVal = max(y)
    z_maxVal = max(z)
    X_scale = math.ceil(X_maxVal/10)
    y_scale = math.ceil(y_maxVal/10)
    z_scale = math.ceil(z_maxVal/10)
    total = len(X)

    #adding 3D grid
    create2DGrid("Y-Z", 10, (0, 0, 0), (math.radians(0), math.radians(-90), math.radians(0)), 11, 11)
    create2DGrid("X-Y", 10, (0, 0, 0), (math.radians(0), math.radians(0), math.radians(0)), 11, 11)
    create2DGrid("Z-X", 10, (0, 0, 0), (math.radians(90), math.radians(0), math.radians(0)), 11, 11)

    #numbering X-axis, y-axis and z-axis
    for num in range(11):    
        textObj(int(num*X_scale), "X_plot", (num, -1, 0), (math.radians(0),math.radians(0),math.radians(90)),textScale=(0.4,0.4,0.4))
        textObj(int(num*y_scale), "y_plot", (0, num, -1), (math.radians(90),math.radians(0) ,math.radians(90)),textScale=(0.4,0.4,0.4)) 
        textObj(int(num*z_scale), "z_plot", (0, -1, num), (math.radians(90),math.radians(0),math.radians(90)),textScale=(0.4,0.4,0.4))
    
    #plotting
    for itr in range(total):
        #plotting sphere
        bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=6, radius=0.2, enter_editmode=False, align='WORLD', location=(X[itr]/X_scale,y[itr]/y_scale,z[itr]/z_scale))

        bpy.context.active_object.name = "scatter "+str(itr)
        
    bpy.ops.object.select_all(action = 'DESELECT')
        
if __name__ == "__main__":
    init()
