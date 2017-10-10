import platform
import os


class System:
    """
    A class abstracting system variables
    """

    """The name of the system the python process is running on"""
    name = platform.node()

    """The operating system"""
    system = platform.system()

    """The id of the current process"""
    pid = os.getpid()

    """The current working dir"""
    cwd = os.getcwd()

    @staticmethod
    def is_windows():
        return System.system == "Windows"

    @staticmethod
    def is_linux():
        return System.system == "Linux"

    @staticmethod
    def is_mac():
        return System.system == "Darwin"
