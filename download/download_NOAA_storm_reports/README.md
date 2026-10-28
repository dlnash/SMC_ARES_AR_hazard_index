## Landslides and Floods reported by the NOAA Storm Events Database

### Download data

1. run 'download_NOAA_storm_events.sh`

This script downloads all of the available storm events details in .csv format from https://www.ncdc.noaa.gov/stormevents/ftp.jsp

### Create subset list of landslide dates

2. run `create_csv_reports.py`

This script uses the downloaded data from the National Oceanic and Atmospheric Administration National Centers for Environmental Information (NOAA NCEI) Storm Events Database and creates a .csv with only the events that were either classified as “debris flow”, "flood", or "flash flood", or had the terms “mudslide”, “landslide”, “mass wasting, or “debris flow” in the event or episode narrative for San Mateo County, CA. 