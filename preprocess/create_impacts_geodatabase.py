import os
import sys
from pathlib import Path
import geopandas as gpd
import pandas as pd
import pyogrio

# --- Personal Modules ---
sys.path.append('../modules')
import globalvars

# -------------------------------------------------------------------
# Read landslide data
# -------------------------------------------------------------------
gdb_path = os.path.join(globalvars.path_to_data,
                        "downloads",
                        "CGS_Reported_Landslide_Events2Share.gdb"
                       )

# Pull first layer from the geodatabase
layer = pyogrio.list_layers(gdb_path)[0][0]

# Read layer data
landslides = gpd.read_file(
    gdb_path,
    layer=layer
)

print(f"Total landslides: {len(landslides)}")

# -------------------------------------------------------------------
# Read San Mateo County boundary
# -------------------------------------------------------------------
county_shp = '../data/JURISDICTIONAL_BOUNDARIES/COUNTY_BOUNDARY.shp'
san_mateo = gpd.read_file(county_shp)
san_mateo = san_mateo.to_crs(landslides.crs) # convert to same crs as landslides

# -------------------------------------------------------------------
# Spatially subset landslides to San Mateo County
# -------------------------------------------------------------------

landslides_sm = gpd.sjoin(
    landslides,
    san_mateo,
    how="inner",
    predicate="within"
)

print(f"Landslides in San Mateo County: {len(landslides_sm)}")

# --- Build CGS Impact dataframe ---

cgs_impact_ids = []
for i in range(0, len(landslides_sm)):
    num = str(i).zfill(3)
    cgs_impact_ids.append(f"CGS_{num}")
    
cgs_impacts = pd.DataFrame({
    'impact_id': cgs_impact_ids,
    'source': "CGS",
    'date': landslides_sm['EVENT_DATE'],
    'latitude': landslides_sm['LAT'],
    'longitude': landslides_sm['LONG'],
    'impact_type': "Landslide",
    'impact_subtype': landslides_sm['REPORTED_LS_TYPE'],
    'geometry': landslides_sm['geometry'],
})

# --- NOAA Storm Reports ---
fname = '../out/noaastormevents_SAN_MATEO_COUNTY_FLOOD_LANDSLIDES.csv'
storm_reports = pd.read_csv(fname)

# ------------------------------------------------------------
# Convert NOAA timestamps from PST (UTC-8) to UTC
# ------------------------------------------------------------

storm_reports['BEGIN_DATE_TIME'] = pd.to_datetime(
    storm_reports['BEGIN_DATE_TIME'],
    errors='coerce'
)

# Localize timestamps to fixed UTC-8 (PST), then convert to UTC
storm_reports['BEGIN_DATE_TIME'] = (
    storm_reports['BEGIN_DATE_TIME']
    .dt.tz_localize('Etc/GMT+8')
    .dt.tz_convert('UTC')
)

# ------------------------------------------------------------
# Build NOAA impacts dataframe
# ------------------------------------------------------------

noaa_impact_ids = [
    f"NOAA_{i:03d}"
    for i in range(len(storm_reports))
]

noaa_impacts = pd.DataFrame({
    'impact_id': noaa_impact_ids,
    'source': "NOAA",
    'date': storm_reports['BEGIN_DATE_TIME'],
    'latitude': storm_reports['BEGIN_LAT'],
    'longitude': storm_reports['BEGIN_LON'],
    'impact_type': storm_reports['EVENT_TYPE'],
    'impact_subtype': None,
})

noaa_gdf = gpd.GeoDataFrame(
    noaa_impacts,
    geometry=gpd.points_from_xy(
        noaa_impacts['longitude'],
        noaa_impacts['latitude']
    ),
    crs='EPSG:4326'
)

noaa_gdf = noaa_gdf.to_crs(landslides.crs)

cgs_impacts['date'] = pd.to_datetime(
    cgs_impacts['date'],
    utc=True,
    errors='coerce'
)

noaa_impacts['date'] = pd.to_datetime(
    noaa_impacts['date'],
    utc=True,
    errors='coerce'
)

# --- Combine CGS and NOAA dfs ---
impacts = gpd.GeoDataFrame(
    pd.concat([cgs_impacts, noaa_gdf], ignore_index=True),
    geometry='geometry',
    crs=landslides.crs
)

# --- filter out of county events again since NOAA storm reports had some --- 
impacts = gpd.sjoin(
    impacts,
    san_mateo,
    how="inner",
    predicate="within"
)

# --- Reproject Everything to WGS84 ---
plot_crs = 'EPSG:4326'
impacts_plot = impacts.to_crs(plot_crs)


# --- Save geodatabase with projected layer and wgs84 layer ---
impacts.to_file(
    '../out/san_mateo_impacts.gpkg',
    layer='impacts_projected',
    driver='GPKG'
)

impacts_plot.to_file(
    '../out/san_mateo_impacts.gpkg',
    layer='impacts_wgs84',
    driver='GPKG'
)
