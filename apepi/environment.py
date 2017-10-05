from tempfile import NamedTemporaryFile


class Environment:
    """
    Used to setup a bash environment and run commands. This is especially useful for module
    environments common on super computing system. An environment file might look like
    this:

        #!/usr/bin/env bash
        module purge
        module load craype-haswell
        module load craype-network-infiniband
        module load mvapich2gdr_gnu/2.1_cuda_7.0
        module load GCC/4.9.3-binutils-2.25
        module load cray-libsci_acc/3.3.0

    The command to be executed would then be appended to the end of the modules.
    """
    def __init__(self, filename=""):
        """
        Constructs the environment. If no # is in the front of the file, a bash file is assumed
        and a bash fileheader is prepended to the environment.

        :param filename: environment file (typically a bash script)
        """
        self.__fileheader = "#!/usr/bin/env bash\n"
        if filename is "":
            self.__env = self.__fileheader
        else:
            self.__env = self.__create_environment(filename)

    def run(self, cmd: str, working_dir=".") -> (str, str, int):
        """
        Run cmd under the environment
        :param cmd: Command to be run
        :param working_dir: working directory. Default "."
        :return: Result of the execution (stdout, stderr, return code)
        """
        tmpfile = self.__create_cmd_file(cmd)
        self.__file_set_execbit(tmpfile.name)

        from os import environ
        from subprocess import Popen, PIPE

        with Popen(tmpfile.name,
                   stdout=PIPE,
                   stderr=PIPE,
                   universal_newlines=True,
                   cwd=working_dir,
                   env=environ.copy()) as p:
            out, err = p.communicate()
            returncode = p.returncode

        return out, err, returncode

    def __create_environment(self, file: str) -> str:
        """
        Create the environment

        If the file does not contain a hash tag in the front, prepend a bash fileheader
        :param file: File where the environment is stored
        :return: The environment stored as a string
        """
        with open(file) as f:
            data = f.read()
        if not data.startswith("#"):
            data = self.__fileheader + data
        return data

    def __create_cmd_file(self, cmd: str) -> NamedTemporaryFile:
        """
        Create the command file by append the cmd to the environment file read before.
        :param cmd: Command to be executed
        :return: A temporary file containing the command
        """
        file = NamedTemporaryFile()
        with open(file.name, 'w') as f:
            f.write(self.__env + "\n")
            f.write(cmd)
        return file

    @staticmethod
    def __file_set_execbit(file: str):
        """
        Set the executable bit on a file
        :param file: The file where the executable bit should be set
        """
        from os import chmod, stat
        st = stat(file)
        chmod(file, st.st_mode | 0o111)


