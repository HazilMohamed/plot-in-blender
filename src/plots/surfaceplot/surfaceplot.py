from surface_gradient_material import SurfaceGradientMaterial
from principle_material import PrincipleMaterial
from common_tools import CommonTools
import bpy
import bmesh
import sys
import math
import json

sys.path.append("src/classes/common_tools")
sys.path.append("src/classes/materials")


class SurfacePlot(CommonTools):
    """
    ===========
    SURFACEPLOT
    ===========
    Surface plots are diagrams of three-dimensional data. 
    It shows a functional relationship between a designated dependent variable (z), 
    and two independent variables (x and y).
    Inheritted Class:
        CommonTools             : It consists of basic operations needed for plotting.
    Imported Class:
        PrincipleMaterial   : Used to create principle material.
    Arguments :
        z                       : The m*n array of values passed by user. It must be of number data type.
        grid_material           : The material color for grid in plot. Default color is White.
        number_material         : The material color for numbers in plot. Default color is White.
        gradient                : The gradient shader of surface.
    Methods:
        surfaceplot             : The main function to plot.
    """

    def __init__(
            self, z, grid_material, number_material, gradient):
        self.z = z
        self.grid_material = grid_material
        self.number_material = number_material
        self.gradient = gradient

    def surfaceplot(self):
        # To delete default objects
        self.clear_screen()

        # Variables used in the function.
        # x and y are obtained from length of 2D array.
        x = len(self.z[0])
        y = len(self.z)
        z_max_val = max(list(map(max, self.z)))
        z_scale = math.ceil(z_max_val/10)
        x_scale = math.ceil(x/10)
        y_scale = math.ceil(y/10)

        # Switching to material mode.
        self.change_viewport(shading="MATERIAL")

        # Adding 3 2D grids for 3D space.
        self.create_2D_grid(
            grid_name="Y_Z", grid_size=10, grid_pos=(0, 0, 0),
            grid_rot=(math.radians(0), math.radians(-90), math.radians(0)),
            x_sub=11, y_sub=11, grid_material=self.grid_material)
        self.create_2D_grid(
            grid_name="X_Y", grid_size=10, grid_pos=(0, 0, 0),
            grid_rot=(math.radians(0), math.radians(0), math.radians(0)),
            x_sub=11, y_sub=11, grid_material=self.grid_material)
        self.create_2D_grid(
            grid_name="Z_X", grid_size=10, grid_pos=(0, 0, 0),
            grid_rot=(math.radians(90), math.radians(0), math.radians(0)),
            x_sub=11, y_sub=11, grid_material=self.grid_material)

        # Numbering x-axis, y-axis and z-axis.
        for num in range(x//x_scale):
            self.text_obj(
                text=int(num*x_scale), text_type="X_plot",
                text_pos=((10/(x-1))*num*x_scale, -1, 0),
                text_rot=(math.radians(0), math.radians(0), math.radians(90)),
                text_scale=(0.4, 0.4, 0.4), number_material=self.number_material)
        for num in range(y//y_scale):
            self.text_obj(
                text=int(num*y_scale), text_type="y_plot",
                text_pos=(0, (10/(y-1))*num*y_scale, -1),
                text_rot=(math.radians(90), math.radians(0), math.radians(90)),
                text_scale=(0.4, 0.4, 0.4), number_material=self.number_material)
        for num in range(11):
            self.text_obj(
                text=int(num*z_scale), text_type="z_plot",
                text_pos=(0, -1, num),
                text_rot=(math.radians(90), math.radians(0), math.radians(90)),
                text_scale=(0.4, 0.4, 0.4), number_material=self.number_material)

        # Adding grid as surface.
        bpy.ops.mesh.primitive_grid_add(
            size=10, location=(5, 5, 0), x_subdivisions=x, y_subdivisions=y)
        bpy.ops.object.transform_apply(
            location=True, rotation=True, scale=True)
        activeObject = bpy.context.active_object
        material = SurfaceGradientMaterial(self.gradient)
        activeObject.data.materials.append(material.create_surface_material())
        bpy.context.active_object.name = "Surface"
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None

        # Plotting the values by moving grid vertices in given z axis.
        # First, make z in a single list.
        flat_z = [item for sublist in self.z for item in sublist]
        z_count = 0

        # Moving each vertex in Z axis.
        for v in bm.verts:
            v.select = True
            bpy.ops.transform.translate(
                value=(0, 0, flat_z[z_count]/z_scale),
                orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
            z_count += 1
            v.select = False

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        return


if __name__ == "__main__":
    # Json parsing.
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    plot = SurfacePlot(
        z=argv["z"], grid_material=argv["grid_material"],
        number_material=argv["number_material"], gradient=argv["gradient"],)
    plot.surfaceplot()
