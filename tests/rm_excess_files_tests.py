from nose.tools import *
import argparse
import os
import tempfile

import rm_excess_files as r

dir(r)

def test_glob_matching():
    d = tempfile.mkdtemp()
    #d.flush()
    #os.fsync(d)
    testglob = os.path.join(d,"match*.tar.gz.gpg")
    testfile = os.path.join(d,"matchblahblah.tar.gz.gpg")
    with open(testfile,"w") as f:
        f.write("some content\n")
    assert_equal(r.matchedfiles(testglob)[0],testfile)





