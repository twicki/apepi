from apepi import Environment
from tempfile import NamedTemporaryFile

def write_file(string: str) -> NamedTemporaryFile:
    """
    Write a file
    :param file content:
    :return: File
    """
    file = NamedTemporaryFile(mode='w')
    with open(file.name, 'w') as f:
        f.write(string)
    return file

def create_env() -> Environment():
    """
    Create a simple environment guaranteed to run on most bash environments
    :return: File
    """
    my_env = """#!/usr/bin/env bash
    """
    file = write_file(my_env)
    return Environment(file.name)

def test_echo():
    """
    Test a simple echo
    """
    env = create_env()

    std, err, code = env.run("echo foobar")
    assert(code == 0)
    assert(std == "foobar\n")
    assert(err == "")

def test_bad_exit():
    """
    Test a bad exit
    """
    env = create_env()
    std, err, code = env.run("exit 1")
    assert (code == 1)
