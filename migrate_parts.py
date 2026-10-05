import snc_utils
import google_drive
import re
import pprint

snc_charts = snc_utils.get_snc_charts()

pprint.pprint (snc_charts)
print(str(len(snc_charts)) + " charts found in SNC.")

chairs_dirs = ["trumpet1"]

for chair in chairs_dirs:
    # job 1 is to clean up the file names for comparison
    # perhaps a function here to take the chair dir and return a dictionary
    # the dictionary would have the padded number as the key
    # this will pick up some crud, but we'll just have to see
    # we could use the dictionary to track our progress on migrating the files themselves
    disco_files = google_drive.discover_files(chair)
    #print(disco_files)

    # perhaps we could just compare the snc parts dict to
    # the discovered files dict instead of using just the file names

    for chart in snc_charts:
        #print (f'{chart} is {snc_charts[chart]['u_slug']}')
        if  chart in disco_files:
            #print (f"file found for chart {chart} - {disco_files[chart]}")
            print (f"{disco_files[chart]} is {chart} which becomes {chart}-{chair}-{snc_charts[chart]['u_slug']}.pdf")
        else:
            print (f"No file found for chart {chart}")

