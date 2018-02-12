##database_polygon=vector
##gps_points=vector
##gps_value_field=string
##id_field=string

from osgeo import ogr
from qgis.utils import iface

bd = database_polygon
gps = gps_points
gps_value_fld = str(gps_value_field)
id_field = str(id_field)

ds_bd = ogr.Open(bd, 1)
ly_bd = ds_bd.GetLayer(0)

nch = ogr.FieldDefn(gps_value_fld, ogr.OFTInteger)
ly_bd.CreateField(nch)

nch2 = ogr.FieldDefn('errors', ogr.OFTString)
ly_bd.CreateField(nch2)

ds_gps = ogr.Open(gps, 0)
ly_gps = ds_gps.GetLayer(0)

i = 0
new_gps_pts = []
for bd_feature in ly_bd:
    bd_feature_geom = bd_feature.GetGeometryRef()
    for gps_feature in ly_gps:
        gps_feature_geom = gps_feature.GetGeometryRef()
        if bd_feature_geom.Contains(gps_feature_geom):
            i += 1
            gps_feature_field = gps_feature.GetFieldAsInteger(gps_value_fld)
            new_gps_pts.append(gps_feature.GetFID())
    if i == 1:
        bd_feature.SetField(gps_value_fld, gps_feature_field)
    if i > 1:
        bd_feature.SetField(gps_value_fld, 99999)
        bd_feature.SetField('errors', 'part')

    if i == 0:
        bd_feature.SetField(gps_value_fld, 0)
    ly_bd.SetFeature(bd_feature)
    ly_gps.ResetReading()
    i = 0

for gps_feature in ly_gps:
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

        out_feat = ogr.Feature(ly_bd.GetLayerDefn())
        out_feat.SetGeometry(poly)
        out_feat.SetField(gps_value_fld, gps_feature.GetFieldAsInteger(gps_value_fld))
        out_feat.SetField('errors', 'redraw')
        [out_feat.SetField(fld, 0) for fld in range(1, out_feat.GetFieldCount() - 2)]
        ly_bd.CreateFeature(out_feat)

ly_bd.ResetReading()

idx = 0
for f in ly_bd:
    f.SetField(id_field, idx)
    g = f.GetGeometryRef()
    idx += 1
    ly_bd.SetFeature(f)

ds_bd = None
ds_gps = None

layer = iface.addVectorLayer(bd, "new_shapefile", "ogr")