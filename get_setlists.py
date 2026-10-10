import snc_utils
import google_drive
import config
import setlist_formatters
import re
from pprint import pprint


item_selector = 1
gigs_with_setlists = snc_utils.get_gigs_with_setlist()
list_choices = {}
gig_sys_id = ""

print (f"{len(gigs_with_setlists)} gigs found with setlists. Choose by number")
for gig in gigs_with_setlists:
    list_choices[str(item_selector)] = gig
    print (f"[{item_selector}] - {gigs_with_setlists[gig]['u_gig.u_name']}")
    item_selector += 1


#print (f"{list_choices}")
gig_choice = input("enter the item number: ")
gig_choice_id = ""

if gig_choice.isdigit() and gig_choice in list_choices:
    gig_choice_id = list_choices[gig_choice]
else:
    print(f"{gig_choice} is not one of the choices.")
    exit(1)

print (f"You chose {gigs_with_setlists[gig_choice_id]['u_gig.u_name']}")
print (f"Writing setlist files to {config.setlist_root}")

#gig_sys_id = "f4bb673f935283d0cf84f677dd03d6c6"
gig_sys_id = gig_choice_id

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
