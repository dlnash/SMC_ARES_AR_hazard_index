import os
import sys
from pathlib import Path
import geopandas as gpd
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature

# --- Personal Modules ---
sys.path.append('../modules')
import globalvars
from plotter import draw_basemap, set_font, plot_terrain

# -------------------------------------------------------------------
# Read San Mateo County boundary
# -------------------------------------------------------------------
plot_crs = 'EPSG:4326'
county_shp = '../data/JURISDICTIONAL_BOUNDARIES/COUNTY_BOUNDARY.shp'
san_mateo = gpd.read_file(county_shp)
san_mateo_plot = san_mateo.to_crs(plot_crs)

# -------------------------------------------------------------------
# Read Impacts Geodatabase 
# -------------------------------------------------------------------

impacts_plot = gpd.read_file(
    '../out/san_mateo_impacts.gpkg',
    layer='impacts_wgs84'
)

noaa = impacts_plot[impacts_plot['source'] == 'NOAA'].copy()
cgs = impacts_plot[impacts_plot['source'] == 'CGS'].copy()

impact_colors = {
    'Debris Flow': '#B5A18A',
    'Flash Flood': '#4F81A8',
    'Flood': '#76B7D4',
    'Hail': '#8A8A8A',
    'Heavy Rain': '#234A78',
    'Landslide': '#8C5A3C'
}

datacrs = ccrs.PlateCarree()
mapcrs = ccrs.Mercator()
extent = [-122.75, -122., 37.05, 37.75]
xticks = np.arange(extent[0], extent[1] + 0.2, 0.2)
yticks = np.arange(extent[2] - 0.5, extent[3] + 0.1, 0.1)

# ---------------------------------------------------------------------
# Create Figure and GridSpec Layout
# ---------------------------------------------------------------------
current_dpi=300
base_dpi=100
scaling_factor = (current_dpi / base_dpi)**0.3
set_font(current_dpi, scaling_factor)
fig = plt.figure(figsize=(8, 9), dpi=current_dpi)
gs = gridspec.GridSpec(
    nrows=1, ncols=2,  # one for map, one for colorbar
    width_ratios=[1, 0.04],  # colorbar narrower
    wspace=0.05
)

# Main map axis
ax = fig.add_subplot(gs[0, 0], projection=mapcrs)

# Colorbar axis
cax = fig.add_subplot(gs[0, 1])

# ---------------------------------------------------------------------
# Plot Data
# ---------------------------------------------------------------------
# Draw base map
ax = draw_basemap(
    ax, extent=extent, xticks=xticks, yticks=yticks,
    left_lats=True, right_lats=False,
    mask_ocean=False, coastline=False
)

ax.set_extent(extent, crs=datacrs)  # extent in lon/lat degrees
ax.set_aspect('auto')  # or 'equal' if you want correct lat/lon ratio

# Plot topography
ax, cs = plot_terrain(ax, extent, vmax=850, greyscale=True)

for impact_type, group in noaa.groupby('impact_type'):

    ax.scatter(
        group['longitude'],
        group['latitude'],
        s=95,
        alpha=0.95,
        color=impact_colors[impact_type],
        edgecolor='white',
        linewidth=0.5,
        transform=datacrs,
        label=impact_type,
        zorder=201
    )

# CGS landslides
ax.scatter(
    cgs.geometry.x.to_numpy(),
    cgs.geometry.y.to_numpy(),
    s=95,
    facecolors='none',
    edgecolors=impact_colors['Landslide'],
    linewidths=2.,
    marker='o',
    transform=ccrs.PlateCarree(),
    label='Landslide',
    zorder=202
)

# Plot SMC Boundary
feature = ShapelyFeature(san_mateo_plot.geometry, ccrs.PlateCarree(),
                         edgecolor='k', facecolor='none', linewidth=1.)
ax.add_feature(feature, zorder=200)

leg = ax.legend(
    loc='upper left',
    fontsize=9,
    frameon=True,
    title='Impact Type'
)

leg.get_title().set_fontweight('bold')
    
# ---------------------------------------------------------------------
# Colorbar and Save Figure
# ---------------------------------------------------------------------
cb = fig.colorbar(cs, cax=cax, orientation='vertical')
cb.set_label('Elevation (m)', fontsize=11)
cb.ax.tick_params(labelsize=10)

output_path = Path('../figs/topographic_map.png')
fig.savefig(output_path, bbox_inches='tight', dpi=fig.dpi)

print(f"Saved figure to: {output_path.resolve()}")