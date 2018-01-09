##parcelles=vector
##gps_terrain=vector
##new_fld=string


from osgeo import ogr
import os

id_fld = "id_match"

ds_parcelles = ogr.Open(parcelles, 1)
ly_parcelles = ds_parcelles.GetLayer(0)

nch = ogr.FieldDefn(new_fld, ogr.OFTInteger)
ly_parcelles.CreateField(nch)

ds_gps_terrain = ogr.Open(gps_terrain, 0)
ly_gps_terrain = ds_gps_terrain.GetLayer(0)

i = 0
for parcelles_feature in ly_parcelles:
    parcelles_feature_geom = parcelles_feature.GetGeometryRef()
    for gps_feature in ly_gps_terrain:
        gps_feature_geom = gps_feature.GetGeometryRef()
        if parcelles_feature_geom.Contains(gps_feature_geom):
            i += 1
            gps_feature_field = gps_feature.GetFieldAsInteger(new_fld)

    if i == 1:
        parcelles_feature.SetField(new_fld, gps_feature_field)
        ly_parcelles.SetFeature(parcelles_feature)
    elif i > 1:
        parcelles_feature.SetField(new_fld, 99999)
        ly_parcelles.SetFeature(parcelles_feature)
    ly_gps_terrain.ResetReading()
    i = 0

ds_parcelles = None
ds_gps_terrain = None




