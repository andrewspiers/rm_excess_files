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
import glob
import logging
import os
import sys


class RemovalCandidate(object):
    """each removal candidate has three attributes: a path (an absolute
    filename), and two properties from os.stat of that filename, mtime and
    size.
    """

    def __init__(self, path):
        self.path = path
        self.stat = os.stat(self.path)
        self.statvfs = os.statvfs(self.path)
        self.mtime = self.stat.st_mtime
        self.size = self.stat.st_size
        self.fsid = self.stat.st_dev  # device
        #available bytes  = blocksize * avail bytes
        self.availbytes = self.statvfs.f_bsize * self.statvfs.f_bavail


def candidates(list_paths):
    """given a list of file paths, return a list of RemovalCandidate(s).
    The list should be sorted with from youngest (at [0], to oldest.
    """
    out = [RemovalCandidate(i) for i in list_paths]
    out.sort(key=lambda x: x.mtime)
    return out

#no test for this one yet
def commonfs(candidates):
    """given a list of RemovalCandidate(s), return True if each Candidate
    comes from the same filesystem.
    """
    firstfsid = candidates[0].fsid
    out = True
    for i in candidates:
        if i.fsid != firstfsid:
            out = False
    return out


def matchedfiles(g):
    """given a glob (g), return the matched files."""
    return glob.glob(g)


def buildparser():
    """build an ArgumentParser object with all the arguments and return it."""
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
    parser.add_argument("--buffer", default=0, type=float,)
    parser.add_argument("--dryrun", action='store_true')
    return parser

def main(args):
    """given an argparse.Namespace (compulsory), process the arguments  within.
    """
    matches = matchedfiles(args.glob)
    sys.stderr.write("using glob " + args.glob + "\n")
    logger.info("using glob " + args.glob + "\n")
    if len(matches) < 1:
        sys.stderr.write("No matches found.\n")
        sys.exit(1)
    c = candidates(matches)
    if not commonfs(c):
        sys.stderr.write("Removal candidates do not all come from the same")
        sys.stderr.write(" file system. Aborting.")
        sys.exit(1)
    requiredbytes = c[-1].size * ( 1 + args.buffer )
    removalrequired = False
    if requiredbytes > c[-1].availbytes:
        removalrequired = True
    if removalrequired:
        print ("Removal is required.")
        print ("Removal candidate  is ", c[:-1].path)
    if args.dryrun:
        print ("This is a dry run, not removing files.")
    else:
        os.remove(c[-1].path)


# Always want to start logging, whether we are __main__ or not.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = buildparser()
    args = parser.parse_args()
    main(args)
