import snc_utils
import google_drive
import config
import setlist_formatters
import re
from pprint import pprint

gig_sys_id = "f4bb673f935283d0cf84f677dd03d6c6"

raw_set_list = snc_utils.get_setlist_by_gig(gig_sys_id)

datestring = raw_set_list['gig_date']
gigname = raw_set_list['gig_name']
gigname = re.sub(r"on \d{4}-\d{2}-\d{2}$", "", gigname)
gigname = re.sub(r"\s*", "", gigname)

for chair in config.chair_dirs:
    fs = setlist_formatters.forscore_setlist(raw_set_list,chair)
    ms = setlist_formatters.mobilesheets_setlist(raw_set_list,chair)

    with open(f"{config.setlist_root}{chair}/{datestring}-{gigname}-{chair}.4ss", "w", encoding="utf-8") as file:
        file.write(fs)
    with open(f"{config.setlist_root}{chair}/{datestring}-{gigname}-{chair}.mss", "w", encoding="utf-8") as file:
        file.write(ms)
       
    #print (fs)
    #print (ms)
