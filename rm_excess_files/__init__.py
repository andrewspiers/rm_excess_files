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


class RemovalCandidate(object):
    """each removal candidate has three attributes: a path (an absolute
    filename), and two properties from os.stat of that filename, mtime and
    size.
    """

    def __init__(self, path):
        self.path = path
        self.stat = os.stat(self.path)
        self.mtime = self.stat.st_mtime
        self.size = self.stat.st_size


def candidates(list_paths):
    """given a list of file paths, return a list of RemovalCandidate(s).
    The list should be sorted with from youngest (at [0], to oldest.
    """
    out = [RemovalCandidate(i) for i in list_paths]
    out.sort(key=lambda x: x.mtime)
    return out


def matchedfiles(g):
    """given a glob (g), return the matched files."""
    return glob.glob(g)


def main(args):
    """given an argparse.Namespace (compulsory), process the arguments  within.
    """
    matches = matchedfiles(args.glob)
    if len(matches) < 1:
        sys.stderr.write('No matches found.')
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--glob",
            help="file glob to match. This should include the whole path"
            "with wildcards as wanted. For example:"
            "\n\t --glob=/backup/backup*.tar.gz.gpg"
            "\n Defaults to current working directory +"
            " 'backup*.tar.gz.gpg'. Take care to protect wildcards from shell"
            " expansion.",
            default=os.path.join(os.getcwd(), "backup*.tar.gz.gpg")
                        )
    parser.add_argument("--preserve", default=1, type=int,
            help="The number of files to preserve.")
    parser.add_argument("--dryrun", action='store_true')
    args = parser.parse_args()
    main(args)
