#!/usr/bin/env python
# coding: utf-8

import os
import re
import html
import string
from time import strptime
from pybtex.database.input import bibtex
import pybtex.database.input.bibtex 

# Primary publication mapping configurations
publist = {
    "journal": {
        "file": "pubs.bib",
        "venuekey": "journal",
        "venue-pretext": "",
        "collection": {"name": "publications", "permalink": "/publication/"}
    } 
}

for pubsource in publist:
    # Define standard month strings as macros to protect pybtex from crashing
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec",
              "july", "august", "september", "october", "november", "december"]
    
    # Initialize parser configuration instance
    parser = bibtex.Parser()
    
    # Inject macro definitions to prevent unquoted month string exceptions
    for m in months:
        parser.macros[m] = m
        parser.macros[m.upper()] = m
        parser.macros[m.capitalize()] = m

    # Parse the target bib file directly using the macro rules
    bibdata = parser.parse_file(publist[pubsource]["file"])

    # Loop through individual entries in the database file
    for bib_id in bibdata.entries:
        pub_year = "1900"
        pub_month = "01"
        pub_day = "01"
        
        b = bibdata.entries[bib_id].fields
        
        try:
            pub_year = f'{b["year"]}'

            # Format publication date targets safely
            if "month" in b.keys(): 
                if len(b["month"]) < 3:
                    pub_month = "0" + b["month"]
                    pub_month = pub_month[-2:]
                elif b["month"] not in range(12):
                    tmnth = strptime(b["month"][:3], '%b').tm_mon   
                    pub_month = "{:02d}".format(tmnth) 
                else:
                    pub_month = str(b["month"])
            if "day" in b.keys(): 
                pub_day = str(b["day"])
                
            pub_date = pub_year + "-" + pub_month + "-" + pub_day
            
            # Format clean titles and sanitize text symbols
            clean_title = b["title"].replace("{", "").replace("}", "").replace("\\", "").replace(" ", "-")    
            url_slug = re.sub("\\[.*\\]|[^a-zA-Z0-9_-]", "", clean_title)
            url_slug = url_slug.replace("--", "-")

            md_filename = (str(pub_date) + "-" + url_slug + ".md").replace("--", "-")
            html_filename = (str(pub_date) + "-" + url_slug).replace("--", "-")

            # Initialize clear clean text citation mapping
            citation = ""

            # Extract author listings safely
            if "author" in bibdata.entries[bib_id].persons:
                for author in bibdata.entries[bib_id].persons["author"]:
                    first = author.first_names[0] if author.first_names else ""
                    last = author.last_names[0] if author.last_names else ""
                    citation = citation + " " + first + " " + last + ", "

            # Append publication title cleanly
            sanitized_title = b["title"].replace("{", "").replace("}", "").replace("\\", "")
            citation = citation + '"' + sanitized_title + '."'

            # Append publication venue metadata parameters
            venue = publist[pubsource]["venue-pretext"] + b[publist[pubsource]["venuekey"]].replace("{", "").replace("}", "").replace("\\", "")
            citation = citation + " " + venue + ", " + pub_year + "."

            # Clean and sanitize quote markers to ensure strict YAML validation bounds pass
            yaml_title = sanitized_title.replace('"', '\\"')
            yaml_citation = citation.replace('"', '\\"')

            ## Construct YAML Front Matter Content Block
            md = "---\n"
            md += 'title: "' + yaml_title + '"\n'
            md += "collection: " + publist[pubsource]["collection"]["name"] + "\n"
            md += "permalink: " + publist[pubsource]["collection"]["permalink"] + html_filename + "\n"
            md += "date: " + str(pub_date) + "\n"
            md += "venue: '" + venue.replace("'", "\\'") + "'\n"
            
            if "url" in b.keys() and len(str(b["url"])) > 5:
                md += "paperurl: '" + b["url"] + "'\n"

            md += 'citation: "' + yaml_citation + '"\n'
            md += "---\n\n"  # Closes header block with zero dirty description append blocks

            md_filename = os.path.basename(md_filename)

            # Output clean individual page profiles safely
            with open("../_publications/" + md_filename, 'w', encoding="utf-8") as f:
                f.write(md)
                
            print(f'SUCCESSFULLY PARSED {bib_id}: "', b["title"][:60], "..."*(len(b['title'])>60), '"')
            
        except KeyError as e:
            print(f'WARNING Missing Expected Field {e} from entry {bib_id}: "', b["title"][:30], "..."*(len(b['title'])>30), '"')
            continue

