##parcelles=vector
##gps_terrain=vector
##gps_value_fld=string

from osgeo import ogr
from qgis.utils import iface

gps_value_fld = str(gps_value_fld)

ds_parcelles = ogr.Open(parcelles, 1)
ly_parcelles = ds_parcelles.GetLayer(0)

nch = ogr.FieldDefn(gps_value_fld, ogr.OFTInteger)
ly_parcelles.CreateField(nch)

nch2 = ogr.FieldDefn('errors', ogr.OFTString)
ly_parcelles.CreateField(nch2)

ds_gps_terrain = ogr.Open(gps_terrain, 0)
ly_gps_terrain = ds_gps_terrain.GetLayer(0)

i = 0
new_gps_pts = []
for parcelles_feature in ly_parcelles:
    parcelles_feature_geom = parcelles_feature.GetGeometryRef()
    for gps_feature in ly_gps_terrain:
        gps_feature_geom = gps_feature.GetGeometryRef()
        if parcelles_feature_geom.Contains(gps_feature_geom):
            i += 1
            gps_feature_field = gps_feature.GetFieldAsInteger(gps_value_fld)
            new_gps_pts.append(gps_feature.GetFID())
    if i == 1:
        parcelles_feature.SetField(gps_value_fld, gps_feature_field)
    if i > 1:
        parcelles_feature.SetField(gps_value_fld, 99999)
        parcelles_feature.SetField('errors', 'part')

    if i == 0:
        parcelles_feature.SetField(gps_value_fld, 0)
    ly_parcelles.SetFeature(parcelles_feature)
    ly_gps_terrain.ResetReading()
    i = 0

for gps_feature in ly_gps_terrain:
    if gps_feature.GetFID() not in new_gps_pts:
        geom = gps_feature.GetGeometryRef()
        x, y = geom.GetX(), geom.GetY()
        ring = ogr.Geometry(ogr.wkbLinearRing)
        u = 20
        ring.AddPoint(x + u, y + u)
        ring.AddPoint(x - u, y + u)
        ring.AddPoint(x - u, y - u)
        ring.AddPoint(x + u, y - u)
        ring.CloseRings()
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        out_feat = ogr.Feature(ly_parcelles.GetLayerDefn())
        out_feat.SetGeometry(poly)
        out_feat.SetField(gps_value_fld, gps_feature.GetFieldAsInteger(gps_value_fld))
        out_feat.SetField('errors', 'redraw')
        [out_feat.SetField(fld, 0) for fld in range(1, out_feat.GetFieldCount() - 2)]
        ly_parcelles.CreateFeature(out_feat)

ds_parcelles = None
ds_gps_terrain = None

layer = iface.addVectorLayer(parcelles, "new_parcelles", "ogr")
