######################################################################
# Filename:    create_AR_impacts_dataframe.py
# Author:      Deanna Nash dnash@ucsd.edu
# Description: Script to create .csv of start and stop times of ARs in San Mateo County and globally
#
######################################################################

import os
import sys
from pathlib import Path
import geopandas as gpd
import numpy as np
import xarray as xr
from datetime import datetime, timedelta
import pandas as pd

# --- Personal Modules ---
sys.path.append('../modules')
import globalvars
from read_data import read_AR_data

# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------
def parse_arid(arid):
    """
    Parse ARID into its encoded start time and object number.

    Example:
        200001100004
        -> 2000-01-10 00Z
        -> object 04
    """
    
    arid = int(arid)  # cast defensively
    s = f"{arid:012d}"
    start_time = datetime.strptime(s[:10], "%Y%m%d%H")
    id0 = int(s[-2:])
    return start_time, id0

def get_ar_lifetimes(ds_global, ds_smc, arid, max_hours=14*24):
    """
    Get full-domain and SMC lifetimes for one ARID.

    Returns
    -------
    ar_start : datetime-like
        First time ARID exists anywhere in the global domain.
    ar_end : datetime-like
        Last time ARID exists anywhere in the global domain.
    smc_start : datetime-like
        First time ARID occurs within SMC.
    smc_end : datetime-like
        Last time ARID occurs within SMC.
    """

    # ARID encodes its approximate start time
    start_time, _ = parse_arid(arid)

    end_time_guess = start_time + timedelta(hours=max_hours)

    # ---------------------------------------------------------------
    # Full-domain AR lifetime
    # ---------------------------------------------------------------

    ds_window = ds_global.sel(
        time=slice(start_time, end_time_guess)
    )

    present_global = ds_window.kidmap == arid

    # AR exists anywhere in global domain at each timestep
    present_global = present_global.any(
        dim=("lat", "lon")
    )

    present_global = present_global.load()

    times_global = ds_window.time.where(
        present_global,
        drop=True
    )

    if len(times_global) == 0:
        return None

    ar_start = times_global.min().values
    ar_end = times_global.max().values

    # ---------------------------------------------------------------
    # SMC AR lifetime
    # ---------------------------------------------------------------

    ds_smc_window = ds_smc.sel(
        time=slice(start_time, end_time_guess)
    )

    present_smc = ds_smc_window == arid

    present_smc = present_smc.any(
        dim=("lat", "lon")
    )

    present_smc = present_smc.load()

    times_smc = ds_smc_window.time.where(
        present_smc,
        drop=True
    )

    if len(times_smc) == 0:
        return None

    smc_start = times_smc.min().values
    smc_end = times_smc.max().values

    return {
        "ARID": arid,
        "ar_start": ar_start,
        "ar_end": ar_end,
        "smc_start": smc_start,
        "smc_end": smc_end,
    }

# -------------------------------------------------------------------
# Read Impacts Geodatabase 
# -------------------------------------------------------------------

impacts = gpd.read_file(
    '../out/san_mateo_impacts.gpkg',
    layer='impacts_wgs84'
)

# -------------------------------------------------------------------
# Read ARDT (Guan and Waliser, 2024) and subset to ext
# -------------------------------------------------------------------

fname = (
    globalvars.path_to_data
    + "downloads/globalARcatalog_ERA5_1940-2024_v4.0.nc"
)

# SMC subset
AR_smc = read_AR_data(
    ar_filename=fname,
    multifile=False,
    varname="kidmap"
)

# Keep only AR grid cells
kidmap_smc = AR_smc.where(
    AR_smc > 0,
    drop=True
)

# AR IDs occurring in SMC
arids = np.unique(
    kidmap_smc.values[
        ~np.isnan(kidmap_smc.values)
    ]
)

print(f"Number of ARs intersecting SMC: {len(arids)}")
print(arids[:10])

# -------------------------------------------------------------------
# Load global ARDT once lazily
# -------------------------------------------------------------------

ds_global = xr.open_dataset(
    fname,
    decode_times=True
)[["kidmap"]]

ds_global = (
    ds_global
    .isel(lev=0, ens=0)
    .squeeze()
    .chunk({"time": 24})
)

# -------------------------------------------------------------------
# Calculate AR lifetimes
# -------------------------------------------------------------------

events = []

for i, arid in enumerate(arids):

    print(
        f"Processing AR {i + 1}/{len(arids)}: "
        f"{int(arid)}"
    )

    event = get_ar_lifetimes(
        ds_global,
        kidmap_smc,
        arid
    )

    if event is not None:
        events.append(event)

# -------------------------------------------------------------------
# Create AR database
# -------------------------------------------------------------------

ar_database = pd.DataFrame(events)


# Calculate durations
ar_database["ar_duration_hr"] = (
    ar_database["ar_end"] -
    ar_database["ar_start"]
).dt.total_seconds() / 3600

ar_database["smc_duration_hr"] = (
    ar_database["smc_end"] -
    ar_database["smc_start"]
).dt.total_seconds() / 3600

ar_database["arid_start"] = pd.to_datetime(
    ar_database["ARID"].astype("int64").astype(str).str[:10],
    format="%Y%m%d%H"
)

# Sort chronologically
ar_database = ar_database.sort_values(
    "smc_start"
).reset_index(drop=True)

# -------------------------------------------------------------------
# Save
# -------------------------------------------------------------------

output_path = "../out/san_mateo_ar_database.csv"

ar_database.to_csv(
    output_path,
    index=False
)

print(f"\nSaved AR database to: {output_path}")

print("\nAR database:")
print(ar_database.head())