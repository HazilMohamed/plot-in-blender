## plot-in-blender
### What it is ?
This is a python library to analyse data, so far the following plots can be visualized in Blender. 
- BarPlot
- ScatterPlot (2D and 3D)
- HistPlot
- SurfacePlot


<p align="center"><img src="https://raw.githubusercontent.com/hazilMohamed/data-visualization-using-blender/master/res/screenshots/3D-Plots.png"></p>

### Requirements
- Blender 2.82 or higher.
- Python 3.8x.

### Setup
- Clone the repo to your directory.
- Change the BLENDER_PATH to your blender executable.

### Import
Import the library to your project
```shell
import plotinblender as bl
```

### Usage
The plotinblender accepts both lists and numpy arrays as arguments
```python
import numpy as np
X = np.array(np.random.rand(500)*500)
y = np.array(np.random.rand(500)*500)
z = np.array(np.random.rand(500)*500)
```
To plot, use the following functions:
- BarPlot
```python
# The Material args are optional to use.
# The Material tuple is in the format (Red, Green, Blue, Alpha).

bl.barPlot(X=X, y=y, gridMaterial = (1,1,1,1), numberMaterial = (1,1,1,1), barMaterial = (1,0,0,1))
```
- ScatterPlot
```python
# The Material args are optional to use.
# The Material tuple is in the format (Red, Green, Blue, Alpha).
# Two arguments gives 2D plots while Three gives 3D plots.
# The cat is optional argument used for categorical plotting.

bl.scatterPlot(X=X, y=y, cat=["Group 1","Group 2"], gridMaterial = (1,1,1,1), numberMaterial = (1,1,1,1))
bl.scatterPlot(X=X, y=y, z=z, cat=["Group 1","Group 2"], gridMaterial = (1,1,1,1), numberMaterial = (1,1,1,1))
```
- HistPlot
```python
# The Material, Bins args are optional to use.
# The Material tuple is in the format (Red, Green, Blue, Alpha).
# The cat is optional argument used for categorical plotting.

bl.histPlot(X=X, bins=35,cat=["Group 1","Group 2"], gridMaterial = (1,1,1,1), numberMaterial = (1,1,1,1))
```
- SurfacePlot
```python
# SurfacePlot requires 2D arrays of size m*n.
# The Material args are optional to use.
# The Material tuple is in the format (Red, Green, Blue, Alpha).

arr = np.arange(20).reshape(4,5)
bl.surfacePlot(z=arr, gridMaterial = (1,1,1,1), numberMaterial = (1,1,1,1), surfaceMaterial = (1,0,0,1))
```
### Contribute
If you have a new idea for plotting or find out a bug or something, please feel free to raise an issue or pull request.

### TODO
- ~~Materials for objects in Blender.~~
- ~~Categorical plots.~~
- Need to implement plots for negative values too.
- Planning to implement an FBX viewer for viewing plots.

