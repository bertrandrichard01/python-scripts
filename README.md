# Add data to database

This script was made in a context of remote sensing for agriculture monitoring, in order to add field data (GPS points) in a multiannual shapefile (polygon) and help in photointerpretation step to finally produce sampling data for training and validation.

## What does the script do?

### 1. Create a field for the new year and a field “errors” 

### 2. Add data in functions of 3 possible cases:

#### Case 1: the plot of land geometry is unchanged
Condition: Only one GPS point is contained in the polygon.
Set the new land use code in the new year field.

#### Case 2: the plot of land has been cut this year
Condition: More than one GPS point is find in a polygon
Write “part” in “errors” field and set “999999” in the new year field. Manually part the polygon and set the new codes.

#### Case 3: appearance of a new plot of land
Condition: The GPS point is not contained in any polygon
Create a new entity by drawing a new polygon (square), write “redraw” in “errors” field and set the new land use code in the new year field, also set 0 to the others years (no data). Manually redraw the polygon.

## Using
- Use this script directly in python

or

- Import in Qgis as a personal toolbox
