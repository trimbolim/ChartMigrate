import snc_utils
import google_drive
import config
import re
#import pycpdflib
from pprint import pprint

core_chairs = [
    "trumpet1",
    "trumpet2",
    "trumpet3",
    "trumpet4",
    "trombone1",
    "trombone2",
    "trombone3",
    "trombone4",
    "alto1",
    "alto2",
    "tenor1",
    "tenor2",
    "bari",
    "guitar",
    "piano",
    "bass",
    "drums",
]

snc_charts = snc_utils.get_snc_charts()

# init cpdf lib
#pycpdflib.loadDLL("/usr/local/lib/libpycpdf.so")

#pprint (snc_charts)
#print(str(len(snc_charts)) + " charts found in SNC.")

disco_file_count = {} 
for chart in snc_charts:
    #print(f"checking {chart}")
    disco_file_count[chart] = [] 

for chair_dir in config.chair_dirs:
    #print(f"checking {chair_dir}")
    file_list = google_drive.get_file_list(chair_dir)
    #print (f"got {len(file_list)} files")

    for chart in snc_charts:
        for file in file_list:
            if chart in file:
                disco_file_count[chart].append(chair_dir)

outlist = []
print (f"count,chart_num,chart_slug,missing_parts")

for chart in disco_file_count:
    difference = list(set(core_chairs) - set(disco_file_count[chart]))
    #difference = list(set(disco_file_count[chart]) ^ set(core_chairs))
    print (f"{len(disco_file_count[chart])},{chart},{snc_charts[chart]['u_slug']},{"|".join(difference)}")
    #outlist.append(f"{len(disco_file_count[chart])} {chart}-{snc_charts[chart]['u_slug']}")
