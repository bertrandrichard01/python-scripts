# Add data to multi-year database

This script was made in a context of remote sensing for agriculture monitoring, in order to add field data (GPS points) in a multi-year shapefile (polygon) and help in photo-interpretation step to finally produce sampling data for training and validation.

## What does the script do?

### 1. Create a field for the new year land use codes and a field “errors” to help the photo-interpreter make manual changes

### 2. Add data in functions of 4 possible cases:

#### Case 1: the plot of land geometry is unchanged
Condition: Only one GPS point is contained in the polygon.

Set the new land use code in the new year field.

#### Case 2: the plot of land has been cut this year
Condition: More than one GPS point is find in a polygon

Write “part” in “errors” field and set “999999” in the new year field. Manually part the polygon and set the new codes.

#### Case 3: appearance of a new plot of land
Condition: The GPS point is not contained in any polygon

Create a new entity by drawing a new polygon (square), write “redraw” in “errors” field and set the new land use code in the new year field, also set 0 to the others years (no data). Manually redraw the polygon.

#### Case 4: no data for the plot of land this year
Condition: No point is found in a polygon.

Set 0 in the new year field (no data).

### 3. Add an ID to each polygon in the new database

## Using
- Use this script directly in python

or

- Import in Qgis as a personal toolbox
