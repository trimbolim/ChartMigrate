from pathlib import Path
import re
import config
import filecmp
import pycpdflib

def get_file_list(chair_dir):

    # iterate through the files in chair_dir and return a dictionary of 
    # filenames and discovered chairs indexed by the 3 digit chart number
    chair_path = config.dest_parts_root + chair_dir

    files_only = [item for item in Path(chair_path).iterdir() if item.is_file()]

    file_list = []

    for file in files_only:
        if not file.name.endswith("pdf"):
            continue
        file_list.append(file.name)

    return file_list


def discover_files(chair_dir, root_dir):

    # iterate through the files in chair_dir and return a dictionary of 
    # filenames and discovered chairs indexed by the 3 digit chart number
    chair_path = root_dir + chair_dir

    files_only = [item for item in Path(chair_path).iterdir() if item.is_file()]
    disco_files = {}

    disco_chair = ""
    homeless_files = [] 

    #print (f"inspecting {chair_dir}")

    for file in files_only:
        if not file.name.endswith("pdf"):
            continue
        #print (f"inspecting {file.name} in {chair_dir}")

        disco_chair = ""
        if chair_dir in file.name:
            #print (f"chair name {chair_dir} in filename {file.name}!")
            disco_chair = chair_dir
        else:
            #print ("try to derive from filename")
            disco_chair = chair_from_filename(file.name)
            #print (f"derived {disco_chair} from {file.name}")
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
            disco_files[disco_chartnum][disco_chair]['src_dir'] = f"{root_dir}{chair_dir}/"
        # if we have seen this chartnum yet we may not have seen it for this chair
        elif disco_chair not in disco_files[disco_chartnum]:
            disco_files[disco_chartnum][disco_chair] = {}
            disco_files[disco_chartnum][disco_chair]['filename'] = file.name
            disco_files[disco_chartnum][disco_chair]['src_dir'] = f"{root_dir}{chair_dir}/"
        else:
            print (f"######### while in {chair_dir} I found a part for {disco_chair} ########")
            print (f'WARN: I already have a key for {disco_chartnum}-{disco_chair}: {file.name}')
            print (f'existing filename: {disco_files[disco_chartnum][disco_chair]['filename']}')
            thisfile = f"{root_dir}{chair_dir}/{file.name}"
            thatfile = f"{root_dir}{chair_dir}/{disco_files[disco_chartnum][disco_chair]['filename']}"
            if filecmp.cmp(thisfile,thatfile):
                print ("but the duplicate is the same file")
            else:
                print ("but they are not the same file")


    return disco_files,homeless_files

def chair_from_filename(fname):

    chair = ""
    file_chair_num = ""
    # I should do the searches for chair identifiers here
    # has_tpt = True if re.search(r'tpt',file.name.lower()) else False
    tptmatch = re.search(r'tpt\s*?(\d)',fname.lower())
    if tptmatch:
        file_chair_num = tptmatch.group(1)

    tbnmatch = re.search(r'tbn\s*?(\d)',fname.lower())
    if tbnmatch:
        file_chair_num = tbnmatch.group(1)

    if tptmatch and file_chair_num:
        chair = f'trumpet{file_chair_num}'
    elif tbnmatch and file_chair_num:
        chair = f'trombone{file_chair_num}'

    return chair

def chartnum_from_filename(fname):
    # I should do the multiple digits test up here
    digit_groups = re.findall(r'\d+',fname)
    three_digit_match = re.search(r'\b\d{3}\b',fname)
    two_digit_match = re.search(r'\b\d{2}\b',fname)
    three_digit_index = ""
    if three_digit_match: 
        three_digit_index = three_digit_match.group()
    elif two_digit_match:
        three_digit_index = f'{int(two_digit_match.group()):03d}'
    else:
        three_digit_index = chartnum_from_strange_filename(fname)

    chartnum = three_digit_index
    return chartnum

def process_file(source_path,dest_path,snc_chart_data, *, range=None, force=None):
    print (f"take {source_path} and push it to {dest_path} with title: {snc_chart_data['u_title']} ")

    pathobj = Path(dest_path)

    if pathobj.is_file() and not force:
        print (f"{dest_path} exists - skipping ")
        return
    else:
        print (f"{dest_path} doesn't exist?")

    title = snc_chart_data['u_title']
    author = snc_chart_data['u_composer']
    pdfproducer = snc_chart_data['u_arranger'] 
    subject = snc_chart_data['u_style'] 


    destpdf = None

    if range==None:
        destpdf = pycpdflib.fromFile(source_path, "")
    else:
        pdf = pycpdflib.fromFile(source_path, "")
        r = pycpdflib.pageRange(range[0],range[1])
        destpdf = pycpdflib.selectPages(pdf, r)

    pycpdflib.setTitle(destpdf,title)
    pycpdflib.setAuthor(destpdf,author)
    pycpdflib.setProducer(destpdf,pdfproducer)
    pycpdflib.setSubject(destpdf,subject)

    print (f"writing {dest_path}")
    pycpdflib.toFile(destpdf, dest_path, False, False)

    return

def chartnum_from_strange_filename(fname):

    for pattern,chartnum in config.strange_patterns.items():
        #if re.search(r'\b\d{3}\b',fname)
        #print (f"trying pattern: {pattern} against {fname}")
        if re.search(pattern,fname,flags=re.IGNORECASE):
            print (f"got a strange one: {fname} maps to {chartnum}")
            return chartnum

    return
