import bpy
import random
import sys
import json

sys.path.append("src/classes/common_tools")
sys.path.append("src/classes/materials")

from common_tools import CommonTools
from pie_material import PieMaterial

class PiePlot(CommonTools):
    """
    =======
    PIEPLOT
    =======
    A pieplot (or a pie chart) is a circular statistical graphic, 
    which is divided into slices to illustrate numerical proportion.
    Inheritted Class:
        CommonTools         : It consists of basic operations needed for plotting.
    Imported Classes:
        PieMaterial         : The class used to create shader node for plotting.
    Arguments:
        x                   : The array of numerical values.
        y                   : The array of categorical values respected to x array.
    Methods:
        pieplot             : The main function to plot.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def pieplot(self):
        # Delete everything on the screen.
        self.clear_screen()

        # Switching to material mode.
        self.change_viewport(shading="MATERIAL")

        # Variables used in the function.
        percent_of_x = []
        for i in self.x:
            percent_of_x.append(i*100/sum(self.x))

        # Instanciating class "PieMaterial".
        material = PieMaterial(percent_of_x)
        
        # Creating a cylinder for pie plot.
        bpy.ops.mesh.primitive_cylinder_add(
            radius=5, depth=0.7, enter_editmode=False, 
            align='WORLD', location=(0, 0, 0))
        active_object = bpy.context.active_object
        active_object.name = "Pie Plot"
        active_object.data.materials.append(material.create_pie_material())

        bpy.ops.object.select_all(action = 'DESELECT')
        return

if __name__ == "__main__":
    # Json parsing
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    plot = PiePlot(x=argv["x"],y=argv["y"])
    plot.pieplot()