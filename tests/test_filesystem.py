from apepi import Filesystem
from tempfile import TemporaryDirectory


def test_tempdir():
    dir = TemporaryDirectory()
    assert (Filesystem.exists(dir.name))
    assert (Filesystem.isdir(dir.name))
    assert (not Filesystem.isfile(dir.name))


def test_create_dir():
    tmpdir = TemporaryDirectory()

    path = tmpdir.name+"/test"

    Filesystem.mkdir(path=path)
    assert (Filesystem.exists(path))
    assert (Filesystem.isdir(path))
    assert (Filesystem.folder_empty(path))

    assert (not Filesystem.folder_empty(tmpdir.name))


def test_touch():
    tmpdir = TemporaryDirectory()
    path = tmpdir.name+"/test"

    Filesystem.touch(path=path)
    assert (Filesystem.exists(path))
    assert (Filesystem.isfile(path))


def test_link():
    tmpdir = TemporaryDirectory()
    src = tmpdir.name+"/src"
    tgt = tmpdir.name+"tgt"

    Filesystem.touch(path=src)
    assert (Filesystem.exists(src))
    assert (Filesystem.isfile(src))

    Filesystem.link(src, tgt)

def test_exists():
    tmpdir = TemporaryDirectory()
    dir = tmpdir.name
    assert (Filesystem.exists(dir))