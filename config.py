source_parts_root = "/Users/matthewtrimboli/Google Drive/My Drive/Swing Shift/Charts/Parts/"
dest_parts_root = "/Users/matthewtrimboli/Google Drive/My Drive/Swing Shift/Charts/NewParts/"
report_dir = "output/"

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

strange_patterns = {
    r'^0[ .]': '000',
    r'\s0.pdf': '000',
    r'^3[ .]': '003',
    r'\s3.pdf': '003',
    r'^4[ .]': '004',
    r'\s4.pdf': '004',
    r'^6[ .]': '006',
    r'\s6.pdf': '006',
    r'^7[ .]': '007',
    r'\s7.pdf': '007',
    r'^8[ .]': '008',
    r'\s8.pdf': '008',
    r'^9[ .]': '009',
    r'\s9.pdf': '009',
    r'^1b[ .]': '521',
    r'\s1b.pdf': '521',
    r'^1-b[ .]': '521',
    r'\s1-b.pdf': '521',
    r'^1-*?e[ .]': '541',
    r'\s1-*?e.pdf': '541',
    r'^1-*?g[ .]': '551',
    r'\s1-*?g.pdf': '551',
    r'^1-*?s[ .]': '561',
    r'\s1-*?s.pdf': '561'
}