#!/usr/bin/python
# -*- coding: utf-8 -*-

from svg_export import *
import sys
import pickle
import csv, codecs, cStringIO


def check_argv(string, argv):
    if "all" in argv:
        return True
    elif string in argv:
        return True
    else:
        return False


def main(argv):
    if not argv:
        print("""
Please specify one or more of the following components to build:
    all
    huge_map
    white_poster
    glare_poster
    index
    index_all
    csv
    all_sectors
    [any sector name]

You can also provide these options:
    --scientific
        """)
        exit()

    scientific = "--scientific" in argv

    with open("starsom28_centered.pickle", "rb") as f:
        stars = pickle.load(f)

    # height = 50
    # width = int(math.sqrt(2) * height)
    # center_x, center_y = 0, 0  # stars[0].X2d, stars[0].Y2d
    # create_beautiful_svg(stars, "test.svg", width, height,
    # offset_x=int(center_x-width/2.0), offset_y=int(center_y-height/2.0))

    map_width = 848
    map_height = 600

    if check_argv("huge_map", argv):
        # Map of everything
        create_beautiful_svg(stars, "all.svg", 848, 600,
                             0, 0,
                             header=u"Star Map 2D – All Stars",
                             draw_tiles=False)

    if check_argv("white_poster", argv):
        poster_width = 120
        poster_height = int(round(poster_width / 28.0 * 20.0 / math.cos(2.0 * math.pi / 6.0 / 2.0)))
        print("Building white poster with size {}x{}".format(poster_width, poster_height))
        create_beautiful_svg(stars, "starmap2d-bundle/poster.svg", poster_width, poster_height,
                             stars[0].X2d - poster_width / 2, stars[0].Y2d - poster_height / 2,
                             header=u"Star Map 2D – Neigbourhood of Sol",
                             draw_tiles=False)

    if check_argv("glare_poster", argv):
        poster_width = 120
        poster_height = int(round(poster_width / 28.0 * 20.0 / math.cos(2.0 * math.pi / 6.0 / 2.0)))
        print("Building white poster with size {}x{}".format(poster_width, poster_height))
        create_beautiful_svg(stars, "starmap2d-bundle/glare_poster.svg", poster_width, poster_height,
                             stars[0].X2d - poster_width / 2, stars[0].Y2d - poster_height / 2,
                             header=u"Star Map 2D – Neigbourhood of Sol",
                             draw_tiles=False, glare=True)

    height = 25
    width = int(math.ceil(height * math.sqrt(2)))
    overlap_tile_count = 1
    divisions_count = int(math.ceil(map_height / height))
    assert (map_width <= divisions_count * width)
    assert (map_height <= divisions_count * height)

    if check_argv("index", argv):
        with open("starmap2d-bundle/index.md", "w") as f:
            f.write(generate_index(stars, width, height, divisions_count, map_width, map_height,
                                   only_famous=True).encode("utf-8"))
    if check_argv("index_all", argv):
        with open("starmap2d-bundle/index_all.md", "w") as f:
            f.write(generate_index(stars, width, height, divisions_count, map_width, map_height,
                                   only_famous=False).encode("utf-8"))

    if check_argv("csv", argv):
        with open("starmap2d-bundle/stars.csv", "wb") as f:
            writer = UnicodeWriter(f)
            writer.writerow(["HYG_ID",
                             "Name",
                             "Code",
                             "X", "Y",
                             "3D_X", "3D_Y", "3D_Z",
                             "Spectrum",
                             "AbsMag",
                             "ColorIndex",
                             "Habitable"])
            for star in stars:
                assert isinstance(star, Star)
                writer.writerow([str(star.StarID),
                                 star.get_best_human_ident(prefer_proper=True),
                                 star.get_best_human_ident(scientific=True),
                                 str(star.X2d), str(star.Y2d),
                                 str(star.X), str(star.Y), str(star.Z),
                                 star.Spectrum,
                                 str(star.AbsMag),
                                 str(star.ColorIndex),
                                 str(star.habitable)
                                 ])


    for row in range(0, divisions_count):
        for column in range(0, divisions_count):
            # column = 5
            # row = 9
            name = get_sector_name(column, row, divisions_count, divisions_count)
            if not check_argv(name, argv) and not check_argv("all_sectors", argv):
                # print("Not included.")
                continue
            print(name)
            viewport_left = column * width - overlap_tile_count
            viewport_top = row * height - overlap_tile_count
            viewport_width = width + 2 * overlap_tile_count
            viewport_height = height + 2 * overlap_tile_count
            print(viewport_left, viewport_left + viewport_width)
            print(viewport_top, viewport_top + viewport_height)

            # if not (viewport_left <= stars[0].X2d <= viewport_left + width and
            #         viewport_top <= stars[0].Y2d <= viewport_top + height):
            #     continue

            create_beautiful_svg(stars, "starmap2d-bundle/{:02d}-{:02d}-{}.svg"
                                 .format(column + 1, row + 1, name),
                                 viewport_width, viewport_height,
                                 viewport_left, viewport_top,
                                 header=u"Star Map 2D Sector {}"
                                 .format(get_sector_name(column, row,
                                                         divisions_count, divisions_count,
                                                         with_coords=True)),
                                 top=get_sector_name(column, row - 1,
                                                     divisions_count, divisions_count,
                                                     with_coords=True),
                                 bottom=get_sector_name(column, row + 1,
                                                        divisions_count, divisions_count,
                                                        with_coords=True),
                                 left=get_sector_name(column - 1, row,
                                                      divisions_count, divisions_count,
                                                      with_coords=True),
                                 right=get_sector_name(column + 1, row,
                                                       divisions_count, divisions_count,
                                                       with_coords=True),
                                 scientific=scientific)


# Taken from https://docs.python.org/2.7/library/csv.html#examples
class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


if __name__ == "__main__":
    main(sys.argv[1:])