import bpy
import bmesh

class CommonTools():
    def clear_screen(self):
        """
        Delete everything from 3D viewport of Blender. 
        """
        bpy.ops.object.select_all(action = "SELECT")
        bpy.ops.object.delete()
        return

    def change_viewport(self, shading="SOLID"):
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

    def create_2D_grid(
            self, grid_name, grid_size, grid_pos, 
            grid_rot, x_sub, y_sub, grid_material=(1,1,1,1)):
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
            create_material  : The materials were created and assigned if not exist.
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
        self.create_material("GridMaterial", grid_material)
        return

    def create_material(self, material_name,diffuse_color):
        """
        The function creates a material if that material_name doesn't exist, 
        use the material to that object if it's already exists. 
        Arguments:
            material_name    : The name of material to be used.
            diffuse_color    : The (R,G,B,A) value to be given for diffuse material.
        """
        
        mat = bpy.data.materials.get(material_name)
        if mat is None:
            mat = bpy.data.materials.new(material_name)
        activeObject = bpy.context.active_object 
        activeObject.data.materials.append(mat)
        bpy.context.object.active_material.diffuse_color = diffuse_color
        return

    def text_obj(
            self, text, text_type, text_pos, text_rot, 
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
        self.create_material("NumberMaterial",number_material)
        return
    
    def transform(
            self, mode, type, size_bar, 
            x_scale, indices):
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