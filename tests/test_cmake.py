from apepi import CMake, CMakeException
from tempfile import TemporaryDirectory
import logging
logging.basicConfig(level=logging.DEBUG)


def get_current_dir() -> str:
    """Return the directory of the file"""
    import os
    return os.path.dirname(os.path.realpath(__file__))


def test_no_cmake():
    """Test error handling"""
    tmpdir = TemporaryDirectory()

    try:
        cmake = CMake(".", tmpdir.name)
    except CMakeException:
        pass


def test_configure():
    """Test cmake reconfiguration"""
    tmpdir = TemporaryDirectory()

    srcdir = get_current_dir()+"/testdata/cmake"
    config = {}
    cmake = CMake(source_dir=srcdir, build_dir=tmpdir.name, configuration=config)
    cmake.configure(configuration=config)
    cmake.make("-j6")


def test_compilation():
    """Test compilation"""
    tmpdir = TemporaryDirectory()

    srcdir = get_current_dir()+"/testdata/cmake"
    cmake = CMake(source_dir=srcdir, build_dir=tmpdir.name)
    cmake.make("-j6")
