import snc_utils
import google_drive
import config
import re
import pycpdflib
from pprint import pprint

snc_charts = snc_utils.get_snc_charts()

# init cpdf lib
pycpdflib.loadDLL("/usr/local/lib/libpycpdf.so")

#pprint (snc_charts)
print(str(len(snc_charts)) + " charts found in SNC.")

for chair_dir in config.chair_dirs:
    file_not_found = []
    transforms = []
    # job 1 is to clean up the file names for comparison
    # perhaps a function here to take the chair dir and return a dictionary
    # the dictionary would have the padded number as the key
    # this will pick up some crud, but we'll just have to see
    # we could use the dictionary to track our progress on migrating the files themselves
    disco_files,homeless_files = google_drive.discover_files(chair_dir,config.source_parts_root)
    #print(disco_files)

    # perhaps we could just compare the snc parts dict to
    # the discovered files dict instead of using just the file names

    for chart in snc_charts:
        #print (f'{chart} is {snc_charts[chart]['u_slug']}')
        if  chart in disco_files:
            #print (f"file found for chart {chart} - {disco_files[chart]}")
            #print (f"{disco_files[chart]} is {chart} which becomes {chart}-{chair}-{snc_charts[chart]['u_slug']}.pdf")
            for disco_chair in disco_files[chart]:
                src_fn = disco_files[chart][disco_chair]['filename'] 
                src_dir = disco_files[chart][disco_chair]['src_dir'] 
                src_path = src_dir + src_fn

                slug = snc_charts[chart]['u_slug']
                dest_fn = f"{chart}-{disco_chair}-{slug}.pdf"
                dest_path = f"{config.dest_parts_root}{disco_chair}/{dest_fn}"

                chart_data = snc_charts[chart]

                transforms.append(f"{src_fn} is {chart} which becomes {dest_fn}")
                result = google_drive.process_file(src_path,dest_path,chart_data)
        else:
            #print (f"No file found for chart {chart}")
            file_not_found.append(snc_charts[chart]['u_sort_field'] + '-' + snc_charts[chart]['u_slug'])


    with open (f'{config.report_dir}homeless_files_{chair_dir}.txt', 'w') as file:
        for item in homeless_files:
                file.write(f"{item}\n")
    with open (f'{config.report_dir}fileless_charts_{chair_dir}.txt', 'w') as file:
        for item in file_not_found:
                file.write(f"{item}\n")
    with open (f'{config.report_dir}transforms_{chair_dir}.txt', 'w') as file:
        for item in transforms:
                file.write(f"{item}\n")