# Steps to reproduce

1) Connect to Postgis
2) Load counties_5m_shp
3) convert counties_5m_shp to ESPG:54034 - world equal area cylindrical projection. Done to retain area for caluclations
4) Create grid with grid size 1600mx1600m, approximately 1 sq mile.
5) Clip grid to projected ESPG:54034 counties_5m_shp
6) Create additional layer of ESPG:54034 counties_5m_shp and convert polygon to lines
7) Use line layer inprevious step to do differencing on clipped grid. This removes grid areas that are on boundaries of counties.
- Select Features where grid interselts line -> create new layer. USe this to difference.
8) Via virtual layer: Count observation points grouped by geoid,county,state, and species name. Method: https://gis.stackexchange.com/questions/448811/counting-points-per-category-in-polygons-using-qgishttps://gis.stackexchange.com/questions/448811/counting-points-per-category-in-polygons-using-qgis
10) Verify each county/species follows poisson distribution
11) Extrapolate observation for each species and each county using randomly quadrant method.
12) Apply bootstrapping to above for better population estimate
