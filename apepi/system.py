import platform


class System:
    """
    A class abstracting system variables
    """

    """The name of the system the python process is running on"""
    name = platform.node()

    """The operating system"""
    system = platform.system()