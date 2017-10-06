import logging


class Filesystem:
    """
    Filesystem helper class
    """

    @staticmethod
    def rmf(path: str):
        """rm -rf"""

        # See https://stackoverflow.com/questions/2656322/shutil-rmtree-fails-on-windows-with-access-is-denied
        def onerror(func, rpath, exc_info):
            """
            Error handler for ``shutil.rmtree``.

            If the error is due to an access error (read only file)
            it attempts to add write permission and then retries.

            If the error is for another reason it re-raises the error.

            Usage : ``shutil.rmtree(path, onerror=onerror)``
            """
            import os
            import stat
            if not os.access(rpath, os.W_OK):
                # Is the error an access error ?
                os.chmod(rpath, stat.S_IWUSR)
                func(rpath)
            else:
                raise

        import shutil
        shutil.rmtree(path=path, onerror=onerror)

    @staticmethod
    def mkdir(path: str, mode=0o700):
        """Create a directory"""
        logging.debug("Create directory {}".format(path))
        import pathlib
        pathlib.Path(path).mkdir(parents=True, exist_ok=True, mode=mode)

    @staticmethod
    def touch(path: str, mode=0o600):
        """Create empty file"""
        logging.debug("Touching file {}".format(path))
        from pathlib import Path
        Path(path=path).touch(mode=mode, exist_ok=True)

    @staticmethod
    def folder_empty(path: str) -> bool:
        """Check if folder is empty"""
        if not Filesystem.isdir(path):
            raise ValueError("The path {} is not a folder".format(path))
        import os
        return len(os.listdir(path)) == 0

    @staticmethod
    def link(source: str, target: str):
        """Create symlink"""
        logging.debug("Creating a symlink from {target} to {source}".format(target=target, source=source))
        import os.symlink
        os.symlink(source=source, link_name=target)

    @staticmethod
    def exists(path: str) -> bool:
        """Check whether path exists"""
        import os.path
        return os.path.exists(path=path)

    @staticmethod
    def isfile(path: str) -> bool:
        """Check whether a path is a file"""
        if not Filesystem.exists(path):
            raise ValueError("The path {} does not exist".format(path))
        import os.path
        return os.path.isfile(path=path)

    @staticmethod
    def isdir(path: str) -> bool:
        """Check whether a path is a directory"""
        if not Filesystem.exists(path):
            raise ValueError("The path {} does not exist".format(path))
        import os.path
        return os.path.isdir(path)

    @staticmethod
    def set_execbit(file: str):
        """
        Set the executable bit on a file
        :param file: The file where the executable bit should be set
        """
        logging.debug("Setting the executable bit to {}".format(file))
        from os import chmod, stat
        st = stat(file)
        chmod(file, st.st_mode | 0o111)