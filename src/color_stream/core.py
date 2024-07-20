"""core.py is the main tool definition."""

import contextlib
import os
import signal
import subprocess
import sys
from typing import Any, Literal

from . import __version__

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
        msg = f"Invalid stream: {stream}"
        raise ValueError(msg)

    stream_id.write(message)
    stream_id.flush()


def run_command_with_colored_streams(command: str) -> None:
    """Run the given command, coloring the streams."""
    process = subprocess.Popen(
        command,
        shell=True,  # noqa: S602
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        # TODO: stdin
    )

    os.set_blocking(process.stdout.fileno(), False)
    os.set_blocking(process.stderr.fileno(), False)

    def signal_handler(sig_num: int, _frame: Any) -> None:  # noqa: ANN401
        """Pass signals received by the parent process to the child process.

        Exits the parent process with the appropriate signal code.

        """
        os.kill(process.pid, sig_num)
        sys.exit(128 + sig_num)

    signals_to_pass = [signal.SIGINT, signal.SIGTERM]

    # SIGHUP doesn't exist on Windows. Skip it it's unavailable.
    with contextlib.suppress(AttributeError):
        signals_to_pass.append(signal.SIGHUP)

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


def main() -> None:
    """Run the main entry point."""
    usage_str = "Usage: python -m color_stream '<command>'"
    if len(sys.argv) < 2:  # noqa: PLR2004
        print(usage_str)
        sys.exit(1)
    elif len(sys.argv) == 2:  # noqa: PLR2004
        if sys.argv[1] in ("-h", "--help"):
            print(usage_str)
            sys.exit(0)
        elif sys.argv[1] in ("-v", "--version"):
            print(f"color_stream {__version__}")
            sys.exit(0)

    # Join the command arguments
    command = " ".join(sys.argv[1:])
    run_command_with_colored_streams(command)


if __name__ == "__main__":
    main()
