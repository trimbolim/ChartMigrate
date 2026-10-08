# ChartMigrate
Utility to find, rename, insert metadata, and migrate pdfs for Swing Shift charts.

* This utility will be pointed at the ./parts/ root folder 
* It will pull the full list of charts from ServiceNow
* it will descend into the chair folder and obtain the list of discovered files
* It will iterate through the list of charts pulled from ServiceNow(SNC)
* Find the files that match that chart. Many folders have parts for multiple chairs.
* If there is 1 file and the chair name is not implied in the filename
   * figure out the chair name implied in the discovered filename
   * open the discovered file
   * inject pdf metadata
   * formulate new filename
   * write the file to the correct chair directory in the new target directory tree
* If there are chairs implied in the filename and there is just one file for that chart/chair pair
   * figure out the chair name implied in the discovered filename
   * open the discovered file
   * inject pdf metadata
   * formulate new filename
   * write the file to the correct chair directory in the new target directory tree
* if there are more than 1 file for the chart/chair pair
    * add the filenames to the dup list for writing at the end of execution

CLI options
```
--chair limit the actions to one chair folder
--no-copy don't copy the files to the new location
```

## dependencies
https://github.com/coherentgraphics/cpdflib-binary

```
pip install pycpdflib
```
Do:
- done: Restructure disco_files to allow multiple files for one chart_num index. i.e. tpt1 tpt2
- done: move chairs list into config.py
- done: define output dir in config.py - update file writes to use that path
- done: create process_file function
- done: rather than hand compare the remaining dups do a file compare
- do: create a file discovery case for finding a completely valid and finished filename
- do: start adding useful args for spot cleanup rather than full migration
- do: make a chart report that tells us what's missing
- do: make a way for the chart report to update SNC on parts status - u_missing_parts

 
