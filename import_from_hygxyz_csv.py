import csv
from star import Star


def import_from_csv(csv_filename="hygxyz.csv", habcat_filename="APJ-HABCAT2.csv"):

    possibly_habitable_stars = []
    if habcat_filename:
        print("Starting import of possibly habitable stars ({})".format(habcat_filename))
        with open(habcat_filename, "rb") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                possibly_habitable_stars.append(int(row[0]))

    print("Starting import from CSV ({})".format(csv_filename))
    stars = []
    with open(csv_filename, "rb") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the headers
        for i, row in enumerate(reader):
            # Sun is definitely habitable (StarID == 0) and stars mentioned in HABCAT are
            # possibly so.
            habitable = row[0] == "0" \
                    or int(row[1]) in possibly_habitable_stars
            try:
                star = Star(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6],
                        float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]),
                        row[12], float(row[13]), float(row[14]), row[15],
                        float(row[16]) if row[16] != "" else None,
                        float(row[17]), float(row[18]), float(row[19]),
                        float(row[20]), float(row[21]), float(row[22]),
                        None, None, habitable=habitable)
                stars.append(star)
            except ValueError:
                print("Cannot convert row {}: {}".format(i, row))
                raise

    print("Sorting list.")
    stars.sort(key=lambda s: s.Distance)
    return stars
