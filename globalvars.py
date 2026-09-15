"""
Filename:    globalvars.py
Author:      Deanna Nash, dnash@ucsd.edu
Description: global variables such as path_to_data for all scripts
"""
import numpy as np

path_to_data = "/cw3e/mead/projects/cwp140/data/"
path_to_repo = "/cw3e/mead/projects/cwp140/repos/SEAK_AR_impacts/"
path_to_conda = "/home/dnash/miniconda3/envs/SEAK-impacts/bin/python"
GEFS_REALTIME_DIR = "/cw3e/mead/projects/cwp140/data/preprocessed/test_merced_GEFS_data"
GEFS_REALTIME_INDEX_DIR = "/cw3e/mead/projects/cwp140/repos/SMC_ARES_AR_hazard_index/data/cfgrib_index_files"
GEFS_REALTIME_IVT_DIR = "/cw3e/mead/projects/cwp140/data/preprocessed/test_merced_GEFS_data"

## These are for when we move back to merced server
# GEFS_REALTIME_DIR = "/data/projects/external_datasets/GEFS/processed"
# GEFS_REALTIME_IVT_DIR = "/data/projects/derived_products/GEFS_IVT/data"

leads = np.arange(3, 169, 3)