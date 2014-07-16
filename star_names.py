

import urllib2
from bs4 import BeautifulSoup
from star import Star
import re

WHITESPACE_REGEX = re.compile(r'\s+')

def fetch_names(star):
    assert(isinstance(star, Star))
    url = "http://simbad.u-strasbg.fr/simbad/sim-basic?Ident={}&submit=SIMBAD+search".format(
        star.get_simbad_ident()
    )
    # print("Getting {}.".format(url))
    response = urllib2.urlopen(url)
    html = response.read()
    # print("HTML read ({} bytes)".format(len(html)))
    soup = BeautifulSoup(html, "html5lib")

    # get Simba main string id
    basic_data_b = soup.find(text=re.compile("Basic data :")).parent
    for parent in basic_data_b.parents:
        if parent.name == "tr":
            basic_data_tr = parent
            break
    star_name_tr = basic_data_tr
    # Walk the tree until we get to the next TR (there's a NavigableString node between TR elements)
    while star_name_tr is basic_data_tr or star_name_tr.name != "tr":
        star_name_tr = star_name_tr.next_sibling
    star_name_b = star_name_tr.b
    name = star_name_b.get_text().strip()
    name = WHITESPACE_REGEX.sub(' ', name)
    name = name.strip()

    # get all other ids
    other_names = []
    identifiers_header = soup.find(text=re.compile(r"Identifiers \(.+\)"))
    if identifiers_header is not None:
        for parent in identifiers_header.parents:
            if parent.name == "table":
                identifiers_header_table = parent
                break
        all_tables = soup.find_all("table")
        for i, table in enumerate(all_tables):
            if table == identifiers_header_table:
                identifiers_table = all_tables[i+1]
        for tt in identifiers_table.find_all("tt"):
            alt_name = tt.get_text().strip()
            alt_name = WHITESPACE_REGEX.sub(' ', alt_name)
            alt_name = alt_name.strip()
            other_names.append(alt_name)

    else:
        print("No identifiers table found.")

    return name, other_names

if __name__ == "__main__":
    from import_from_hygxyz_csv import import_from_csv
    from star_names import fetch_names
    import time
    import export
    import sys
    stars = import_from_csv()
    for i, star in enumerate(stars[:10000]):
        try:
            print("[{:>12}] Trying {}.".format(i, star))
            name, alt_names = fetch_names(star)
            print("  - {} (and {} alternative names)".format(name, len(alt_names)))
            star.simbad_string_id = name
            star.simbad_identifiers = alt_names
        except KeyboardInterrupt:
            break
        except:
            print("ERROR WHEN GETTING {}".format(star))
            print(sys.exc_info()[0])
            pass
        finally:
            time.sleep(0.5)
    export.export_to_pickle(stars, "10000_stars_with_simbad_names.pickle")