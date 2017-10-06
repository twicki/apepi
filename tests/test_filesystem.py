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
    print(path)

    Filesystem.mkdir(path)
    assert (Filesystem.exists(path))
    assert (Filesystem.isdir(path))


