"""
Main driver for AR hazard processing.
Compute + save
→ AR index
→ save nc
→ save csv
Domain here is used to limit preprocessing of dataset as well as for information on the bounding box on the csv. 
"""

import argparse
import yaml
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor

import grib_helper
from forecast_processor import process_all_variables
from ar_hazard_index import compute_AR_hazard_index
from io_utils import save_processed_datasets
from summaries import export_summary_csv
import globalvars


# ---------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "--init-date",
    required=True,
    help="Initialization date YYYYMMDDHH",
)

parser.add_argument(
    "--domain",
    default="San-Mateo",
)

parser.add_argument(
    "--source",
    default="reforecast",
)

parser.add_argument(
    "--server",
    default="aware",
)

args = parser.parse_args()

init_date = args.init_date
domain_name = args.domain
source = args.source
server = args.server


# ---------------------------------------------------------
# Config
# ---------------------------------------------------------

var_lst = [
    "qpf",
    "ivt",
    "freezing_level",
    "uv",
]

nworkers = 4

# ---------------------------------------------------------
# Load domain config
# ---------------------------------------------------------

with open("config/domain.yaml", "r") as f:
    config = yaml.safe_load(f)

domain_cfg = config["domains"][domain_name]

domain = {
    "lon_min": -179.5,
    "lon_max": -110.,
    "lat_min": 10.,
    "lat_max": 70.,
}


# ---------------------------------------------------------
# Build index files if reading realtime .grb2 files
# ---------------------------------------------------------
if source == "realtime":
    def make_index(lead_time):
        t0 = time.perf_counter()
    
        grib_helper.build_and_save_index_files(
            F=lead_time,
            init_date=init_date,
        )
    
        elapsed = time.perf_counter() - t0
    
        return lead_time, elapsed
    
    
    t00 = time.perf_counter()
    
    with ThreadPoolExecutor(max_workers=nworkers) as executor:
        results = list(
            executor.map(
                make_index,
                globalvars.leads,
            )
        )
    
    total = time.perf_counter() - t00
    
    print("\nIndividual times:")
    for F, elapsed in results:
        print(f"F{F:03d}: {elapsed:.2f} s")
    
    print(f"\nTotal wall time to build index files: {total:.2f} s")
# if source == "realtime":
#     t00 = time.perf_counter()
#     args = (leads, init_date)
    
#     with ThreadPoolExecutor(max_workers=nworkers) as executor:
#         results = list(executor.map(grib_helper.build_and_save_index_files, args))
    
#     total = time.perf_counter() - t00
    
#     print("\nIndividual times:")
#     for F, elapsed in results:
#         print(f"F{F:03d}: {elapsed:.2f} s")
    
#     print(f"\nTotal wall time to build index files: {total:.2f} s")

# ---------------------------------------------------------
# Process variables
# ---------------------------------------------------------
fc, final_ds = process_all_variables(
    init_date=init_date,
    var_lst=var_lst,
    domain=domain,
    source=source,
    server=server,
)


# ---------------------------------------------------------
# Compute AR hazard index
# ---------------------------------------------------------

final_ds = compute_AR_hazard_index(
    final_ds
)

# ---------------------------------------------------------
# Export netCDFs
# ---------------------------------------------------------

save_processed_datasets(
    fc,
    final_ds,
    init_date,
    source,
)

# ---------------------------------------------------------
# Export CSV
# ---------------------------------------------------------

export_summary_csv(
    final_ds,
    domain_name,
    domain_cfg,
    init_date,
    mode="max",
)