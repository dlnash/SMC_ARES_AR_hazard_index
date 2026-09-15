"""
Filename:    test.py
Author:      Deanna Nash, dnash@ucsd.edu
Description: testing parallel writing of custom index files
"""
import time
import gefs_realtime

init_date = '2026091406'
t00 = time.perf_counter()
ds = gefs_realtime.load_realtime_freezing_level(init_date)

print(ds)

print(f"\nTotal time: {time.perf_counter() - t00:.2f} s")

# import os
# import time
# import numpy as np
# import grib_helper
# from concurrent.futures import ThreadPoolExecutor

# base = (
#     "/cw3e/mead/projects/cwp140/data/preprocessed/"
#     "test_merced_GEFS_data/2026091406"
# )


# filters = {
#     "qpf": {
#         "dataType": "pf",
#         "typeOfLevel": "surface",
#         "level:float": 0.0,
#         "paramId": 228228,
#         "shortName": "tp",
#     },
#     "u": {
#         "dataType": "pf",
#         "typeOfLevel": "isobaricInhPa",
#         "shortName": "u",
#         "level:float": 1000.0,
#     },
#     "v": {
#         "dataType": "pf",
#         "typeOfLevel": "isobaricInhPa",
#         "shortName": "v",
#         "level:float": 1000.0,
#     },
#     "freezing_level": {
#         "dataType": "pf",
#         "typeOfLevel": "isothermZero",
#         "level:float": 0.0,
#         "shortName": "gh",
#     },
# }




# t00 = time.perf_counter()

# leads = np.arange(3, 169, 3)
# args = (leads, init_date)

# with ThreadPoolExecutor(max_workers=4) as executor:
#     results = list(executor.map(grib_helper.build_and_save_index_files, args))

# total = time.perf_counter() - t00

# print("\nIndividual times:")
# for F, elapsed in results:
#     print(f"F{F:03d}: {elapsed:.2f} s")

# print(f"\nTotal wall time: {total:.2f} s")


# for name, filter_keys in filters.items():
#     for F in leads:

# def load_xarray_object_from_grb_using_index(F, varname, init_date): 
#     print(f"\n{varname} F{F:03d}:")

#     filter_keys = filters[varname]

#     indexpath = os.path.join(globalvars.GEFS_REALTIME_INDEX_DIR,
#                              f"gefs_{init_date}_F{F:03d}.idx",
#                             )

#     index = grib_helper.load_index(indexpath)

#     subindex = index.subindex(filter_keys)

#     print(f"  Subindex groups: {len(subindex)}")

#     xr_ds = grib_helper.dataset_from_subindex(subindex)

#     return xr_ds

# print(f"\nTotal time: {time.perf_counter() - t00:.2f} s")

# import time
# import xarray as xr
# import numpy as np
# from cfgrib.dataset import open_fileindex
# from cfgrib.messages import FileStream
# from cfgrib.dataset import build_dataset_components
# from cfgrib.dataset import Dataset as CfgribDataset
# import cfgrib
# import cfgrib.xarray_plugin as xarray_plugin
# import cfgrib.dataset
# import cfgrib.messages




# fname = (
#     "/cw3e/mead/projects/cwp140/data/preprocessed/"
#     "test_merced_GEFS_data/2026091406/"
#     "gefs_2026091406_F015.grb2"
# )



# print('Testing standard opening coordinates')

# standard = xr.open_dataset(
#     fname,
#     engine="cfgrib",
#     filter_by_keys=filters["qpf"],
#     backend_kwargs={"indexpath": ""},
#     decode_timedelta=False,
# )

# print(standard["time"].values)
# print(standard["step"].values)
# print(standard["valid_time"].values)

# t00 = time.perf_counter()

# print("Building in-memory index...")


# print(f"Index build time: {time.perf_counter() - t00:.2f} s")

# for name, filter_keys in filters.items():

#     print(f"\n{name}:")

#     subindex = index.subindex(filter_keys)

#     print(f"  Subindex groups: {len(subindex)}")

#     dimensions, variables, attributes, encoding = build_dataset_components(
#         subindex,
#         errors="warn",
#         encode_cf=("parameter", "time", "geography", "vertical"),
#     )
    
#     # Build the cfgrib Dataset container
#     cf_ds = cfgrib.dataset.Dataset(
#         dimensions,
#         variables,
#         attributes,
#         encoding,
#     )
    
#     # Wrap it for xarray
#     store = SimpleDataStore(cf_ds)
    
#     # Construct actual xarray Dataset
#     xr_ds = xr.Dataset(
#         store.get_variables(),
#         attrs=store.get_attrs(),
#     )
    
#     print(xr_ds)

#     # Identify the primary meteorological variable
#     data_vars = [
#         v for v in xr_ds.data_vars
#         if v not in ["time", "step", "valid_time", "surface",
#                      "isobaricInhPa", "isothermZero"]
#     ]

#     var = data_vars[0]
#     print(f"  Primary variable: {var}")
#     print(f"  Data type before load: {type(xr_ds[var].data)}")

#     t0 = time.perf_counter()
#     xr_ds.load()
#     print(f"  Load time: {time.perf_counter() - t0:.2f} s")
#     print(f"  Data type after load: {type(xr_ds[var].data)}")
#     print(f"  Min/max: {xr_ds[var].values.min()} / {xr_ds[var].values.max()}")

#     xr_ds["valid_time"] = xr_ds["valid_time"].astype("datetime64[s]")
#     xr_ds["time"] = xr_ds["time"].astype("datetime64[s]")

#     print(xr_ds["time"].values)
#     print(xr_ds["step"].values)
#     print(xr_ds["valid_time"].values)

#     if name == 'qpf':
#         test_result = np.testing.assert_allclose(
#     xr_ds["tp"].values,
#     standard["tp"].values,
# )
#         print(f"Testing to see if values are the same: {test_result}")
    

# print(f"\nTotal time: {time.perf_counter() - t00:.2f} s")



# import os
# import time
# from concurrent.futures import ThreadPoolExecutor
# import xarray as xr

# base = "/cw3e/mead/projects/cwp140/data/preprocessed/test_merced_GEFS_data/2026091406"

# leads = [15, 18, 21, 24]

# qpf_filter = {
#     "dataType": "pf",
#     "typeOfLevel": "surface",
#     "level": 0,
#     "paramId": 228228,
#     "shortName": "tp",
# }


# def build_qpf_index(F):
#     fname = os.path.join(
#         base,
#         f"gefs_2026091406_F{F:03d}.grb2",
#     )

#     print(f"Starting F{F:03d}")
#     t0 = time.perf_counter()

#     ds = xr.open_dataset(
#         fname,
#         engine="cfgrib",
#         filter_by_keys=qpf_filter,
#         backend_kwargs={
#             "indexpath": f"{fname}.qpf.idx",
#         },
#         decode_timedelta=False,
#     )

#     ds.close()

#     elapsed = time.perf_counter() - t0
#     print(f"Finished F{F:03d}: {elapsed:.2f} s")

#     return F, elapsed


# t0 = time.perf_counter()

# with ThreadPoolExecutor(max_workers=2) as executor:
#     results = list(executor.map(build_qpf_index, leads))

# total = time.perf_counter() - t0

# print("\nIndividual times:")
# for F, elapsed in results:
#     print(f"F{F:03d}: {elapsed:.2f} s")

# print(f"\nTotal wall time: {total:.2f} s")

# import time
# import xarray as xr

# fname = "/cw3e/mead/projects/cwp140/data/preprocessed/test_merced_GEFS_data/2026091406/gefs_2026091406_F015.grb2"
# index_path = fname + ".shared.idx"

# filters = {
#     "qpf": {
#         "dataType": "pf",
#         "typeOfLevel": "surface",
#         "level": 0,
#         "paramId": 228228,
#         "shortName": "tp",
#     },
#     "u": {
#         "dataType": "pf",
#         "typeOfLevel": "isobaricInhPa",
#         "shortName": "u",
#         "level": 1000,
#     },
#     "v": {
#         "dataType": "pf",
#         "typeOfLevel": "isobaricInhPa",
#         "shortName": "v",
#         "level": 1000,
#     },
#     "freezing_level": {
#         "dataType": "pf",
#         "typeOfLevel": "isothermZero",
#         "shortName": "gh",
#     },
# }

# for name, filter_keys in filters.items():

#     t0 = time.perf_counter()

#     ds = xr.open_dataset(
#         fname,
#         engine="cfgrib",
#         filter_by_keys=filter_keys,
#         backend_kwargs={
#             "indexpath": index_path,
#         },
#         decode_timedelta=False,
#     )

#     open_time = time.perf_counter() - t0

#     print(f"\n{name}:")
#     print(f"  Open time: {open_time:.2f} s")
#     print(f"  Variables: {list(ds.data_vars)}")
#     print(f"  Dimensions: {dict(ds.sizes)}")

#     ds.close()

# import time
# from cfgrib.messages import FileStream, FileIndex
# from cfgrib.dataset import INDEX_KEYS

# fname = "/cw3e/mead/projects/cwp140/data/preprocessed/test_merced_GEFS_data/2026091406/gefs_2026091406_F015.grb2"

# index_path = fname + ".shared.idx"

# t0 = time.perf_counter()

# stream = FileStream(fname)

# index_keys = sorted(set(INDEX_KEYS) | {"time", "step"})

# print("Building shared index...")
# index = FileIndex.from_indexpath_or_filestream(
#     stream,
#     index_keys,
#     indexpath=index_path,
# )

# print(f"Index build time: {time.perf_counter() - t0:.2f} s")
# print(f"Index path: {index_path}")
# print(f"Number of index entries: {len(index)}")
# print(f"Index keys: {index.keys()}")

# import os
# import time
# import xarray as xr
# import numpy as np
# import time

# import gefs_realtime

# fname = "/cw3e/mead/projects/cwp140/data/preprocessed/test_merced_GEFS_data/2026091406/gefs_2026091406_F015.grb2"

# t0 = time.perf_counter()

# ds = xr.open_dataset(
#     fname,
#     engine="cfgrib",
#     filter_by_keys={
#         "dataType": "pf",
#         "typeOfLevel": "surface",
#         "level": 0,
#         "paramId": 228228,
#         "shortName": "tp",
#     },
#     backend_kwargs={
#         "indexpath": "",
#     },
#     decode_timedelta=False,
# )

# print(f"Open time: {time.perf_counter() - t0:.2f} s")

# ds["tp"].load()

# print(f"Total time: {time.perf_counter() - t0:.2f} s")

# ds.close()

# ds = gefs_realtime.load_realtime_freezing_level("2026091406", leads=[6])
# print(ds)

# ds = gefs_realtime.load_realtime_uv("2026091406", leads=[6])
# print(ds)

# ds = gefs_realtime.load_realtime_qpf(
#     "2026091406",
#     leads=np.arange(3, 169, 3),
# )

# print(ds)

# fname = "/cw3e/mead/projects/cwp140/data/preprocessed/test_merced_GEFS_data/2026091406/gefs_2026091406_F006.grb2"

# filters = {
#     "qpf": {
#         "dataType": "pf",
#         "name": "Total Precipitation",
#         "typeOfLevel": "surface",
#         "level": 0,
#         "paramId": 228228,
#         "shortName": "tp",
#     },
#     "u": {
#         "dataType": "pf",
#         "typeOfLevel": "isobaricInhPa",
#         "shortName": "u",
#         "level": 1000,
#     },
#     "v": {
#         "dataType": "pf",
#         "typeOfLevel": "isobaricInhPa",
#         "shortName": "v",
#         "level": 1000,
#     },
#     "freezing_level": {
#         "dataType": "pf",
#         "typeOfLevel": "isothermZero",
#         "shortName": "gh",
#     },
# }

# for varname, filter_keys in filters.items():

#     idx = f"{fname}.{varname}.idx"

#     t0 = time.perf_counter()

#     ds = xr.open_dataset(
#         fname,
#         engine="cfgrib",
#         filter_by_keys=filter_keys,
#         backend_kwargs={"indexpath": idx},
#         decode_timedelta=False,
#     )

#     open_time = time.perf_counter() - t0

#     t0 = time.perf_counter()
#     ds.load()
#     load_time = time.perf_counter() - t0

#     print(f"{varname}: open={open_time:.2f} s, load={load_time:.2f} s")
#     print(ds)

#     ds.close()