from pathlib import Path
import re
import config

def discover_files(chair):

    chair_dir = config.source_parts_root + chair

    files_only = [item for item in Path(chair_dir).iterdir() if item.is_file()]
    disco_files = {}

    for file in files_only:
        groups = re.findall(r'\d+',file.name)

        # cleanest case
        if re.search(r'\d{3}',file.name) and chair in file.name:
            match = re.search(r'\d{3}',file.name)
            #print (f"3 digit index found {str(match.group())}" )
            disco_files[str(match.group())] = file.name
        # messy case
        elif len(groups) > 1:
            print (f"Ambiguous numbering for {file.name}")
            # is it tpt 1
            if re.search(r'tpt',file.name.lower()):
                print ("FOUND tpt")
                if re.search(r'tpt\d',file.name.lower()):
                    match = re.search(r'tpt\d',file.name.lower())
                    print (f"FOUND {str(match.group())}")
                elif re.search(r'tpt\s\d',file.name.lower()):
                    match = re.search(r'tpt\s\d',file.name.lower())
                    print (f"FOUND {str(match.group())}")
                elif re.search(r'solo',file.name.lower()):
                    print (f"FOUND solo")
            # or is it tpt1
            # it it the solo part
            continue
        # just one set of digits - we just pad it and move on
        elif re.search(r'\b\d{1,2}\b',file.name):
            match = re.search(r'\b\d{1,2}\b',file.name)
            padded_num = f'{int(match.group()):03d}'
            disco_files[padded_num] = file.name

    return disco_files