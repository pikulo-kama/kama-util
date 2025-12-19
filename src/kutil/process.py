import os
import sys
import psutil

from kutil.logger import get_logger


_logger = get_logger(__name__)


def get_running_processes(processes: list[str]) -> list[psutil.Process]:
    """
    Used to check if any of the provided processes
    are currently running.

    Will return list of those that are actually running.

    Iterates through the system process list and matches names against the
    provided list. To optimize performance, the scan terminates early once
    all requested processes have been identified.
    """

    running_processes = []

    for process in psutil.process_iter(['name']):
        # No need to continue scanning processes if we already
        # found all that were requested.
        if len(running_processes) == len(processes):
            break

        try:
            if process.name() in processes:
                running_processes.append(process)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return running_processes


def is_process_already_running(process_name: str):
    """
    Used to check if process with provided name already running.
    Will not consider current process if name matches.

    Verifies if another instance of the specified process name is active by
    comparing process IDs and executable paths. This ensures that only
    instances launched from the same executable are flagged as duplicates.
    """

    current_pid = os.getpid()
    _logger.debug("Current PID=%d, Exe=%s", current_pid, sys.executable)

    for process in psutil.process_iter(['name', 'pid', 'exe']):

        try:
            process_exe = process.exe()
            process_exe = os.path.realpath(process_exe) if process_exe else None
            _logger.debug("PID=%d, Name=%s, Exe=%s", process.pid, process.name(), process_exe)

            if process.pid == current_pid:
                continue

            if process_exe != sys.executable:
                continue

            if process.name() == process_name:
                return True

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return False
