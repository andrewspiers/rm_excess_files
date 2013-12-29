#!/usr/bin/python
"""Remove matching files at a given location, to free up space for more.

First, look at the location specified by --location, and find all files
matching --glob. If --location is not specified, use the current
directory. Read their sizes.

Then figure out which filesystem is at location. If there is enough spare room
on the filesystem to write another file equal to the size of the most recent
matching file, plus a buffer percentage (default 0), then do nothing.
Otherwise,  Delete matching files until there is enough space, preserving
--preserve number of matching files (default 0). --dryrun will not delete any
files, but will tell you what it would have deleted.
"""

from rm_excess_files import *


if __name__ == "__main__":
    parser = buildparser()
    args = parser.parse_args()
    main(args)
