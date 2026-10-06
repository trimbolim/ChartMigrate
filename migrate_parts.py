import snc_utils
import google_drive
import re
from pprint import pprint

snc_charts = snc_utils.get_snc_charts()

#pprint (snc_charts)
print(str(len(snc_charts)) + " charts found in SNC.")

chair_dirs = [
    "trumpet1",
    "trumpet2",
    "trumpet3",
    "trumpet4",
    "trumpet5",
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
    "vocal",
    "conductor"
]

for chair in chair_dirs:
    file_not_found = []
    transforms = []
    # job 1 is to clean up the file names for comparison
    # perhaps a function here to take the chair dir and return a dictionary
    # the dictionary would have the padded number as the key
    # this will pick up some crud, but we'll just have to see
    # we could use the dictionary to track our progress on migrating the files themselves
    disco_files,homeless_files = google_drive.discover_files(chair)
    #print(disco_files)

    # perhaps we could just compare the snc parts dict to
    # the discovered files dict instead of using just the file names

    for chart in snc_charts:
        #print (f'{chart} is {snc_charts[chart]['u_slug']}')
        if  chart in disco_files:
            #print (f"file found for chart {chart} - {disco_files[chart]}")
            #print (f"{disco_files[chart]} is {chart} which becomes {chart}-{chair}-{snc_charts[chart]['u_slug']}.pdf")
            transforms.append(f"{disco_files[chart]} is {chart} which becomes {chart}-{chair}-{snc_charts[chart]['u_slug']}.pdf")
        else:
            #print (f"No file found for chart {chart}")
            file_not_found.append(snc_charts[chart]['u_sort_field'] + '-' + snc_charts[chart]['u_slug'])


    with open (f'homeless_files_{chair}.txt', 'w') as file:
        for item in homeless_files:
                file.write(f"{item}\n")
    with open (f'fileless_charts_{chair}.txt', 'w') as file:
        for item in file_not_found:
                file.write(f"{item}\n")
    with open (f'transforms_{chair}.txt', 'w') as file:
        for item in transforms:
                file.write(f"{item}\n")
    #print (f"these files had no home:") 
    #pprint(homeless_files)
    #print (f"these homes had no files:") 
    #pprint(file_not_found)

