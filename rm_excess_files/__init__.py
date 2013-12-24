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

import argparse
import fnmatch
import glob
import os


def main(args):
    """given an argparse.Namespace (compulsory), process the arguments  within.
    """
    matches = glob.glob(args.glob)
    print (matches)

def  matchedfiles(g):
    """given a glob (g), return the matched files."""
    return glob.glob(g)

if  __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--glob",
            help="file glob to match. This should include the whole path"
            "with wildcards as wanted. For example:"
            "\n\t --glob=/backup/backup*.tar.gz.gpg"
            "\n Defaults to current working directory +"
            " 'backup*.tar.gz.gpg'. Take care to protect wildcards from shell"
            " expansion.",
            default=os.path.join(os.getcwd(),"backup*.tar.gz.gpg")
                        )
    parser.add_argument("--preserve", default=1, type=int,
            help="The number of files to preserve.")
    parser.add_argument("--dryrun",action='store_true')
    args  = parser.parse_args()
    main(args)

