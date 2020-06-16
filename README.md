# data-visualization-using-blender
A python tool to analyse data using Blender
## data-visualization-using-blender
### What it is ?
This is a python library to analyse data using Blender, so far the following plots can be visualized. 
- BarPlot
- ScatterPlot (2D and 3D)
- HistPlot


<p align="center"><img src="https://raw.githubusercontent.com/hazilMohamed/data-visualization-using-blender/master/res/screenshots/3D-scatterPlot.png"></p>

### Requirements
- Blender 2.82 or higher.
- Python 3.8x.

### Setup
- Clone the repo to your directory.
- Change the BLENDER_PATH to your blender executable.

### Importing
Import the library to your project
```shell
import plotinblender as bl
```

### Usage
To plot, use the function ``plot``
```python
bl.plot(X,y,plotName="barPlot")                    #For BarPlot
bl.plot(X,y,plotName="scatterPlot")                #For 2D ScatterPlot
bl.plot(X,y,z,plotName="scatterPlot")              #For 3D ScatterPlot
bl.plot(X,bins=20,plotName="countPlot")            #For HistPlot
```

### Contribute
If you have a new idea for plotting or find out a bug or something, please raise an issue or pull request.

### TODO
- Need to implement plots for negative values too.
- Planning to implement an FBX viewer for viewing plots.
- Materials for objects in Blender.
- Categorical plots.

