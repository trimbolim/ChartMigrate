#!/usr/bin/python3

import yaml
import argparse
import logging
import config
import snc_utils
import pycpdflib
import google_drive

parser = argparse.ArgumentParser(description='Split Master PDFs into parts')
parser.add_argument('file_to_split',  type=str, 
                    help='Master PDF to be split.')
parser.add_argument('map_file', help='path to yaml file with parts map', type=str)
parser.add_argument('chartnum', help='3 digit chartnum for output filename', type=str)
parser.add_argument('--title_slug', help='title for output filename', type=str, required=False)
parser.add_argument('--push', help='push files into Swing Shift folders', action='store_true' )
parser.add_argument('--force', help='overwrite any existing files', action='store_true' )

args = parser.parse_args()

pycpdflib.loadDLL("/usr/local/lib/libpycpdf.so")
bigpdf = pycpdflib.fromFile(args.file_to_split, '')

chartnum = args.chartnum
snc_charts = snc_utils.get_snc_charts()
title_slug = snc_charts[chartnum]['u_slug']

with open(args.map_file) as file:
    try:
        chartmap = yaml.safe_load(file)   
    except yaml.YAMLError as exc:
        print(exc)

for chair in chartmap['destinations']['chairs']:
    range = chartmap['destinations']['chairs'][chair]

    outfilename = f"{chartnum}-{chair}-{title_slug}.pdf" 
    outfilepath = f"{config.dest_parts_root}{chair}/{outfilename}"

    if args.push:
        print (f"Pushing {outfilename} to {outfilepath}")
        google_drive.process_file(args.file_to_split, outfilepath, snc_charts[chartnum], range=range, force=args.force)
    else:
        print (f"I would push {outfilename} to {outfilepath}")
