from apepi import System


def test_name():
    import platform
    name = platform.uname()[1]
    assert (name == System.name)


def test_system():
    import platform
    system = platform.system()
    assert (system == System.system)