

class System:
    """
    A class abstracting system functions
    """

    @staticmethod
    def get_name() -> str:
        """Return the name of the system the python process is running on"""
        import platform
        return platform.node()