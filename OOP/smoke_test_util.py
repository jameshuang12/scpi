"""Helper methods for smoke test scripts"""
from __future__ import print_function
import os
from shutil import rmtree
import hashlib
import errno
import subprocess
import datetime
import random
import signal
import socket
import time

MD5HASH_BLOCKSIZE = 8192


# various utilities
def silent_remove(path):
    """Remove the supplied path/file silently; raise an error
       only if it's other than file not found"""
    try:
        os.remove(path)
    except OSError as err:
        if err.errno is not errno.ENOENT:
            raise


def local_print(args, quiet_flag=False):
    """ utility to optionally print out a line """
    if not quiet_flag:
        print(args)


def clear_and_create_directory(directory):
    """ Remove and create a directory """
    if os.path.exists(directory):
        local_print("Clearing directory %s" % directory)
        rmtree(directory)
    os.mkdir(directory)


def clear_directory(directory):
    """ Remove a directory """
    if os.path.exists(directory):
        rmtree(directory)


def run_and_record(command, run_async=False, no_stderr=False, **kwargs):
    """Run the test executable with parameters """
    # Filter out kwargs controlled by this function
    arg_names = ["stdout", "stderr", "bufsize"]
    extra_args = {x: kwargs.get(x) for x in kwargs if x not in arg_names}
    print(" ".join(command))
    if any(x in extra_args for x in arg_names):
        print("Ignoring invalid optional parameter to 'run_and_record'.")
    with open(os.devnull, "w") as tempf:
        # pylint: disable=consider-using-with
        if run_async:
            if no_stderr:
                return subprocess.Popen(command, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, bufsize=0, **extra_args)

            return subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=0, **extra_args)

        return subprocess.call(command, stdout=tempf, **extra_args)


def get_time(filename):
    """Return the most recent time (create/modify)"""
    ctime = datetime.datetime.fromtimestamp(os.path.getctime(filename))
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filename))

    if ctime < mtime:
        return ctime

    return mtime


def get_latest_executable(all_base_paths, filename):
    """Return the most recent/newest version of the supplied filename.
       Checking in all base paths"""
    final_executable = ""

    # initialize to an arbitrary old date older than the current executables
    final_executable_time = datetime.datetime.min

    # loop through all paths, look for the executables, compare times and use the
    # most recent executables to run the tests
    for path in all_base_paths:
        curr_executable = ""

        # see if the current path has the executables
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower() == filename.lower():
                    curr_executable = os.path.join(root, f)

        # the file was found, get the create/modified time
        if curr_executable != "":
            curr_executable_time = get_time(curr_executable)
            # if the current time is newer than the previous, save it
            if curr_executable_time > final_executable_time:
                final_executable_time = curr_executable_time
                final_executable = curr_executable

    return final_executable


def cleanup(out_file):
    """Clean up any resources (files, etc) the application has created"""
    print("Cleaning up test output...")
    try:
        os.remove(out_file)
    except OSError as err:
        if err.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise


def get_md5(file_path):
    """Get the md5 sum for the passed in file name"""
    try:
        md5 = hashlib.md5()
        with open(file_path, 'r') as input_file:
            while True:
                blk = input_file.read(MD5HASH_BLOCKSIZE)
                if not blk:
                    break
                md5.update(blk)
            md5sum = md5.hexdigest()
    except (OSError, IOError):
        md5sum = ''
    return md5sum


def verify_unchanged(input_file, output_file):
    """Verify that two files exactly match"""
    in_md5 = get_md5(input_file)
    out_md5 = get_md5(output_file)

    if in_md5 == out_md5:
        print("SUCCESS: Matched checksums")
        return True

    print("ERROR: Checksums do not match %s != %s" % (in_md5, out_md5))
    return False


def verify_smaller(input_file, output_file):
    """Verify that the output file is smaller than the input"""
    in_size = os.path.getsize(input_file)
    out_size = os.path.getsize(output_file)

    if in_size > out_size:
        print("SUCCESS: Output file was smaller")
        return True

    print("ERROR: Output file was not smaller %s <= %s" % (in_size, out_size))
    return False


def get_random_port():
    """ Generate a random port number """
    return random.randint(1025, 60000)


def does_process_child_exist(executables, process, timeout=10, is_found=True):
    """Checks the process's children to see if a specific child process exists based on the given executable names"""
    end_time = time.time() + timeout
    while True:
        for child in process.children():
            # handle single name or list of multiple names
            if isinstance(executables, str):
                found = (child.exe() == executables)
            else:
                found = (child.exe() in executables)

            if found == is_found or time.time() > end_time:
                return found
        time.sleep(0.1)


def count_occurrences_in_file(file_path, search_string):
    """Counts the number of times the provided string appears in the given log file"""
    with open(file_path) as log_file:
        return sum(search_string in line for line in log_file)


def does_not_contain_error(file_path):
    """Checks that no keytools error log messages are in the given log file"""
    flag = (count_occurrences_in_file(file_path, "[error]") == 0)
    flag &= (count_occurrences_in_file(file_path, " ERROR ") == 0)
    return flag


def wait_for_occurences_in_file(file_path, search_string, timeout=10):
    """Wait for an entry to appear in a file."""
    end_time = time.time() + timeout
    while True:
        occurs = count_occurrences_in_file(file_path, search_string)
        if occurs or time.time() > end_time:
            return occurs
        time.sleep(0.1)


def print_file(file_name):
    """Print contents of given file if it exists."""
    if not os.path.exists(file_name):
        print("Path {} did not exist.".format(file_name))
        return
    print(f'{file_name}:')
    with open(file_name) as f:
        print(f.read())
    print()


def wait_for_service(address, port, timeout=60):
    """Wait for a TCP service to start."""
    end_time = time.time() + timeout
    while time.time() < end_time:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((address, port))
            return
        except ConnectionRefusedError:
            time.sleep(0.1)
            continue
        except Exception as e:
            raise ConnectionError(f'Unexpected error waiting for {address}:{port}') from e
    raise TimeoutError(f'Timeout waiting for {address}:{port}')


def check_and_stop_process(process, name, timeout=60):
    """Check if process is still running and stop it."""
    check_result = process.poll()
    if check_result is not None:
        print(f'{name} failed {check_result}')
        process_out, process_err = process.communicate()
        print(f'{name} stdout:')
        print(process_out)
        print()
        print(f'{name} stderr:')
        print(process_err)
        print()
    else:
        process.send_signal(signal.SIGTERM)
        try:
            result = process.wait(timeout)
            if result != 0:
                print(f'{name} exit value {result}')
        except subprocess.TimeoutExpired:
            print(f'Signal failed to stop {name}, killing')
            process.kill()
