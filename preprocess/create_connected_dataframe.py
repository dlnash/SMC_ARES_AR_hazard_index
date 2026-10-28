import geopandas as gpd
import pandas as pd

# --- load impacts and ar dfs ---
impacts = gpd.read_file(
    '../out/san_mateo_impacts.gpkg',
    layer='impacts_wgs84'
)

ar_df = pd.read_csv('../out/san_mateo_ar_database.csv')

# --- make sure dates are datetimes ---
impacts['date'] = pd.to_datetime(impacts['date'], utc=True, format='mixed')

for col in ['ar_start', 'ar_end', 'smc_start', 'smc_end']:
    ar_df[col] = pd.to_datetime(ar_df[col], utc=True)

# --- make all possible ar - impact combinations ---
impact_ar = impacts[['impact_id', 'date']].merge(
    ar_df[['ARID', 'smc_start', 'smc_end']],
    how='cross'
)

# create relationship column
impact_ar['relationship'] = 'unassociated'

# define during AR as impact when ar was over SMC
during = (
    (impact_ar['date'] >= impact_ar['smc_start']) &
    (impact_ar['date'] <= impact_ar['smc_end'])
)

impact_ar.loc[
    during,
    'relationship'
] = 'during_AR'

# define post AR when impact occurred within 48 hours of AR over SMC
post_48h = (
    (impact_ar['date'] > impact_ar['smc_end']) &
    (impact_ar['date'] <=
     impact_ar['smc_end'] + pd.Timedelta(hours=48))
)

impact_ar.loc[
    post_48h,
    'relationship'
] = 'post_AR'

# define pre AR when impact occurred within 24 hours of AR over SMC
pre_24h = (
    (impact_ar['date'] < impact_ar['smc_start']) &
    (impact_ar['date'] >=
     impact_ar['smc_start'] - pd.Timedelta(hours=24))
)

impact_ar.loc[
    pre_24h,
    'relationship'
] = 'pre_AR'

# keep only rows where AR was associated with impact
ar_impact_df = impact_ar[
    impact_ar['relationship'] != 'unassociated'
].copy()

ar_impact_df['hours_from_smc_start'] = (
    ar_impact_df['date'] -
    ar_impact_df['smc_start']
).dt.total_seconds() / 3600

ar_impact_df['hours_from_smc_end'] = (
    ar_impact_df['date'] -
    ar_impact_df['smc_end']
).dt.total_seconds() / 3600

# keep only columns we want
ar_impact_df = ar_impact_df[
    ['ARID', 'impact_id', 'relationship', 'hours_from_smc_start', 'hours_from_smc_end']
]

# -------------------------------------------------------------------
# Save
# -------------------------------------------------------------------

output_path = "../out/san_mateo_ar-impact_database.csv"

ar_impact_df.to_csv(
    output_path,
    index=False
)

print(f"\nSaved AR-impact database to: {output_path}")