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
    print(f"checking {chart}")
    disco_file_count[chart] = [] 

for chair_dir in config.chair_dirs:
    print(f"checking {chair_dir}")
    # convert this to use google_drive.discover_files() - should be simple
    disco_files,homeless_files = google_drive.discover_files(chair_dir,config.dest_parts_root)
    #file_list = google_drive.get_file_list(chair_dir)
    print (f"got {len(disco_files)} files")

    for chart in snc_charts:
        if chart in disco_files and chair_dir in disco_files[chart]:
            if 'filename' in disco_files[chart][chair_dir]:
                disco_file_count[chart].append(chair_dir)


for chart in disco_file_count:

    difference = list(set(core_chairs) - set(disco_file_count[chart]))
    diff_string = "|".join(sorted(difference))
    chart_uuid = snc_charts[chart]['sys_id']
    snc_missing_parts = snc_charts[chart]['u_missing_parts']
    print (f"diff string for chart {chart} is {diff_string}")

    if not diff_string == snc_missing_parts:
        #print (f"these differ")
        print (f"we say: {diff_string}")
        print (f"snc: {snc_missing_parts}")
        res = snc_utils.update_missing_parts(chart_uuid,diff_string)
        res = True
        if res:
            print (f"updated {chart} with {diff_string}")
        else:
            print ("update failed")
