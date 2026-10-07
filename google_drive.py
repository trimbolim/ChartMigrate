from pathlib import Path
import re
import config

def discover_files(chair_dir):

    # iterate through the files in chair_dir and return a dictionary of 
    # filenames and discovered chairs indexed by the 3 digit chart number
    chair_path = config.source_parts_root + chair_dir

    files_only = [item for item in Path(chair_path).iterdir() if item.is_file()]
    disco_files = {}

    disco_chair = ""
    homeless_files = [] 

    #print (f"inspecting {chair_dir}")

    for file in files_only:
        if not file.name.endswith("pdf"):
            continue
        #print (f"inspecting {file.name} in {chair_dir}")

        # ambiguous case with 3 digit index but multiple digits found
        #elif three_digit_index and len(digit_groups) > 1 and tptmatch and file_chair_num:
            #print (f"Ambiguous numbering for {file.name} but it looks like {three_digit_index} for trumpet{file_chair_num}")

            #if three_digit_index in disco_files:
                #print (f"WARN: Already have a key for {three_digit_index}")
            #else: 
                #disco_files[three_digit_index] = {}
            #disco_files[three_digit_index]['filename'] = file.name
            #disco_files[three_digit_index]['chair'] = f"trumpet{file_chair_num}"

        # messy case when multiple sets of digits are found and none is 3 digit
        #elif len(digit_groups) > 1:
            #print (f"Ambiguous numbering for {file.name}")
        # just one set of digits, no chair
        #elif len(digit_groups) == 1:
            #if three_digit_index in disco_files:
                #print (f"WARN: Already have a key for {three_digit_index}")
            #else: 
                #disco_files[three_digit_index] = {}
            #disco_files[three_digit_index]['filename'] = file.name
        #else:
            #print(f"AMBIGUOUS: Can't decide what to do with {file.name}")
        # don't even call the function if the current chair_dir is in the filename
        if chair_dir in file.name:
            disco_chair = chair_dir
        else:
            disco_chair = chair_from_filename(file.name)
        # if no indicator on chair in filename, assume chair_dir
        if not disco_chair:
            disco_chair = chair_dir

        disco_chartnum = chartnum_from_filename(file.name)

        if not disco_chartnum:
            homeless_files.append(file.name)
        # if we haven't seen this chartnum yet
        elif disco_chartnum not in disco_files:
            disco_files[disco_chartnum] = {}
            #disco_files[disco_chartnum][] = {}
            disco_files[disco_chartnum][disco_chair] = {}
            disco_files[disco_chartnum][disco_chair]['filename'] = file.name
        # if we have seen this chartnum yet we may not have seen it for this chair
        elif disco_chair not in disco_files[disco_chartnum]:
            disco_files[disco_chartnum][disco_chair] = {}
            disco_files[disco_chartnum][disco_chair]['filename'] = file.name
        else:
            print (f'WARN: I already have a key for {disco_chair} {disco_chartnum} {file.name}')
            print (f'WARN: existing entry: {disco_files[disco_chartnum][disco_chair]['filename']}')

    return disco_files,homeless_files

def chair_from_filename(fname):

    chair = ""
    # I should do the searches for chair identifiers here
    # has_tpt = True if re.search(r'tpt',file.name.lower()) else False
    tptmatch = re.search(r'tpt\s*?(\d)',fname.lower())
    file_chair_num = tptmatch.group(1) if tptmatch else None

    if tptmatch and file_chair_num:
        chair = f'trumpet{file_chair_num}'

    return chair

def chartnum_from_filename(fname):
    # I should do the multiple digits test up here
    digit_groups = re.findall(r'\d+',fname)
    three_digit_match = re.search(r'\b\d{3}\b',fname)
    three_digit_index = ""
    if three_digit_match: 
        three_digit_index = three_digit_match.group()
    two_digit_match = re.search(r'\b\d{2}\b',fname)
    if two_digit_match:
        three_digit_index = f'{int(two_digit_match.group()):03d}'
    chartnum = three_digit_index
    return chartnum

def process_file(source_path,dest_path,snc_chart_data):
    pass
    return