from .environment import Environment
from . import Filesystem
import logging
logger = logging.getLogger("apepi.CMake")


class CMakeException(Exception):
    """An exception class that handles cmake exceptions"""

    def __init__(self, message: str, output: str, error: str):
        super(Exception, self).__init__(message)
        print(output)
        print(error)
        self.output = output
        self.error = error


class CMake:
    """A simple CMake wrapper class"""

    def __init__(self, source_dir: str,  build_dir: str,  configuration={},
                 environment=Environment(), overwrite_build_folder=False,
                 cmake_command="cmake", build_command="make"):
        """
        CMake configuration class. Automatically calls the cmake configuration

        :param source_dir: containing CMakeLists.txt
        :param build_dir: build directory
        :param configuration: the cmake configuration, such as CMAKE_INSTALL_PREFIX=directory
        :param environment: environment to the configuration
        :param overwrite_build_folder: replace the build folder in case it already exists
        :param cmake_command: Path to cmake
        :param build_command: Path to make (or cmake depending on your flavor)
        """

        if not Filesystem.isdir(source_dir):
            raise ValueError("CMake: The source directory {} does not exist or is not a path."
                             .format(source_dir))
        if not Filesystem.exists(build_dir):
            raise ValueError("CMake: The build directory {} does not exist.".format(build_dir))
        if not Filesystem.folder_empty(build_dir) and not overwrite_build_folder:
            raise ValueError("CMake: The build directory {} is not empty.".format(build_dir))

        # Cleanup and create dir
        if Filesystem.exists(build_dir) and overwrite_build_folder:
            Filesystem.rmf(build_dir)

        Filesystem.mkdir(build_dir)

        self.environment = environment
        self.source_dir = source_dir
        self.build_dir = build_dir
        self.cmake_command = cmake_command
        self.build_command = build_command

        self.configure(configuration)

    def configure(self, configuration: {}):
        """Configure"""
        arg = CMake.__stringify_configuration(config=configuration)
        cmd = "{cmake} {src} {arg}".format(cmake=self.cmake_command,
                                           src=self.source_dir,
                                           arg=arg)
        logger.info("CMake configure {}\n{}".format(self.build_dir, cmd))
        std, err, code = self.environment.run(cmd=cmd, working_dir=self.build_dir)
        logger.info("\n{output}\n{error}".format(output=std, error=err))

        if code != 0:
            raise CMakeException("Unable to run cmake\n{output}\n{error}", output=std, error=err)

    def make(self, arg=""):
        """Build"""
        cmd = "{make} {arg}".format(make=self.build_command, arg=arg)
        logger.info("CMake in {}\n{}".format(self.build_dir, cmd))
        std, err, code = self.environment.run(cmd=cmd, working_dir=self.build_dir)
        logger.info("\n{output}\n{error}".format(output=std, error=err))

        if code != 0:
            raise CMakeException("Unable to run cmake\n{output}\n{error}", output=std, error=err)

    @staticmethod
    def __stringify_configuration(config: dict) -> str:
        arg = ""
        for key, value in config.items():
            arg += "-D{key}=\"{value}\" ".format(key=key, value=value)
        return arg