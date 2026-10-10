import xml.etree.ElementTree as ET

def mobilesheets_setlist(raw_set_list, chair):

    root = ET.Element("Setlists")
    setlists = ET.SubElement(root, "Setlists")

    for set_pos in sorted(raw_set_list['sets']):
        setlist = ET.SubElement(setlists, "Setlist")
        setlist_name = ET.SubElement(setlist, "Name")
        setlist_name.text = f"{raw_set_list['gig_name']} - Set {set_pos}"

        for list_pos in raw_set_list['sets'][set_pos]['ordered_charts']:

            composed_filename = f"{list_pos['u_chart.u_sort_field']}-{chair}-{list_pos['u_chart.u_slug']}.pdf"
            song = ET.SubElement(setlist, "Song")
            title = ET.SubElement(song, "Title")
            title.text = list_pos['u_chart.u_slug']
            filename = ET.SubElement(song, "FileName")
            filename.text = composed_filename
            filetype = ET.SubElement(song, "FileType")
            filetype.text = "1"

    ET.indent(root, space="  ")

    setlist_string = ET.tostring(root,encoding='unicode',method='xml',short_empty_elements=True, xml_declaration=True)

    return setlist_string

def forscore_setlist(raw_set_list, chair):

    #chair 

    root = ET.Element("forScore", kind="setlist", version="1.0", title=raw_set_list['gig_name'])

    for set_pos in sorted(raw_set_list['sets']):
        placeholder_title = f"Set {set_pos}"
        score = ET.SubElement(root, "placeholder", title=placeholder_title)
        for list_pos in raw_set_list['sets'][set_pos]['ordered_charts']:

            path = f"{list_pos['u_chart.u_sort_field']}-{chair}-{list_pos['u_chart.u_slug']}.pdf"
            placeholder_title = f"MISSING: {list_pos['u_chart.u_sort_field']}-{chair}-{list_pos['u_chart.u_slug']}"
            score = ET.SubElement(root, "score", path=path, title=placeholder_title)

    ET.indent(root, space="  ")

    setlist_string = ET.tostring(root,encoding='unicode',method='xml',short_empty_elements=True,xml_declaration=True)

    return setlist_string