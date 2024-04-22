#!/usr/bin/env python3

import sys
import subprocess
import os
from typing import Literal
import signal

# ANSI escape codes
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def _write_to_stream(
    message: str, stream: Literal["stdout", "stderr"]
) -> None:
    if stream == "stdout":
        stream_id = sys.stdout
    elif stream == "stderr":
        stream_id = sys.stderr
    else:
        raise ValueError(f"Invalid stream: {stream}")

    stream_id.write(message)
    stream_id.flush()


def main():
    if len(sys.argv) < 2:
        print("Usage: python split_colors.py <command>")
        sys.exit(1)

    # Join the command arguments
    command = " ".join(sys.argv[1:])

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        # TODO: stdin
    )

    os.set_blocking(process.stdout.fileno(), False)
    os.set_blocking(process.stderr.fileno(), False)

    def signal_handler(sig_num, frame):
        """Passes signals received by the parent process to the child process.
        Exits the parent process with the appropriate signal code."""
        os.kill(process.pid, sig_num)
        sys.exit(128 + sig_num)

    signals_to_pass = [signal.SIGINT, signal.SIGTERM, signal.SIGHUP]
    for sig in signals_to_pass:
        signal.signal(sig, signal_handler)

    while True:
        while stdout_content := process.stdout.read():
            _write_to_stream(
                f"{GREEN}{stdout_content.decode('utf-8')}{RESET}", "stdout"
            )

        while stderr_content := process.stderr.read():
            _write_to_stream(
                f"{RED}{stderr_content.decode('utf-8')}{RESET}", "stderr"
            )

        if (return_code := process.poll()) is not None:
            sys.exit(return_code)


if __name__ == "__main__":
    main()
