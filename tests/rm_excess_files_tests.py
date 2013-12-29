from nose.tools import *
import argparse
import os
import shutil
import tempfile
import time

import rm_excess_files.rm_excess_files as r

dir(r)

def test_candidates_3files():
    """create 3 files, create a candidates() list out of them, and check that
    the list is comprised of the right number and type of files, and that they
    are ordered from youngest to oldest."""
    #files = [tempfile.mkstemp() for i in range(3)]
    files = []
    for i in range(3):
        files.append(tempfile.mkstemp())
        time.sleep(0.1)  #sleep is essential to ensure mtimes are different.
    paths = [i[1] for i in files]
    candidates = r.candidates(paths)
    assert_is_instance(candidates, list)
    assert_equal(len(candidates),3)
    young = 0.00 #mtime of 0 : created at unix epoch
    assert_greater_equal
    for i in candidates:
        assert_is_instance(i,r.RemovalCandidate)
        assert_greater_equal(i.mtime,young)
        young = i.mtime
    map(os.remove,paths)  #remove the test files


def test_glob_matching():
    d = tempfile.mkdtemp()
    #d.flush()
    #os.fsync(d)
    testglob = os.path.join(d,"match*.tar.gz.gpg")
    testfile = os.path.join(d,"matchblahblah.tar.gz.gpg")
    with open(testfile,"w") as f:
        f.write("some content\n")
    assert_equal(r.matchedfiles(testglob)[0],testfile)
    shutil.rmtree(d)

@raises(SystemExit)
def test_main_dryrun():
    """passing dryrun arg to main function."""
    parser = r.buildparser()
    args = parser.parse_args(['--dryrun'])
    r.main(args)

@raises(SystemExit)
def test_main_noargs():
    """calling main, passing no arguments."""
    startdir = os.getcwd()
    d = tempfile.mkdtemp()
    os.chdir(d)
    parser = argparse.ArgumentParser()
    parser.add_argument('--glob',
            default=os.path.join(os.getcwd(),"backup*.gz.gpg"))
    args=parser.parse_args()
    r.main(args)
    os.chdir(startdir)



def test_RemovalCandidate_instantiation():
    """just test the creation of a RemovalCandidate ojbect"""
    f = tempfile.mkstemp()
    #f[1] is the absolute pathname.
    rc = r.RemovalCandidate(f[1])
    assert_equal(rc.path,f[1])
    assert_is_instance(rc.mtime,float)
    assert_equal(rc.size,0)
    os.remove(f[1])

def test_commonfs_truecase():
    """commonfs should return true when supplied with a list of two
    RemovalCandidates, each with the same fsid."""
    f1 = tempfile.mkstemp()
    f2 = tempfile.mkstemp()
    rc1 = r.RemovalCandidate(f1[1])
    rc2 = r.RemovalCandidate(f2[1])
    assert r.commonfs([rc1,rc2])
