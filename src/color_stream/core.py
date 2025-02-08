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

MAX_READ_SIZE_BYTES: int = 1024 * 1024


def _write_to_stream(
    message: bytes, stream: Literal["stdout", "stderr"]
) -> None:
    if stream == "stdout":
        stream_id = sys.stdout
    elif stream == "stderr":
        stream_id = sys.stderr
    else:
        msg = f"Invalid stream: {stream}"
        raise ValueError(msg)

    os.write(stream_id.fileno(), message)
    stream_id.flush()


def run_command_with_colored_streams(
    command: str, *, enable_byte_count_log_at_end: bool
) -> None:
    """Run the given command, coloring the streams."""
    process = subprocess.Popen(  # noqa: S602
        command,
        shell=True,
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

    total_stdout_bytes = 0
    total_stdout_activations = 0
    total_stderr_bytes = 0
    total_stderr_activations = 0

    while True:
        bytes_since_checking_other_stream = 0
        while (stdout_content := process.stdout.read()) and (
            bytes_since_checking_other_stream < MAX_READ_SIZE_BYTES
        ):
            _write_to_stream(
                GREEN.encode() + stdout_content + RESET.encode(),
                "stdout",
            )
            len_stdout_content = len(stdout_content)
            bytes_since_checking_other_stream += len_stdout_content
            total_stdout_bytes += len_stdout_content
        if bytes_since_checking_other_stream:
            total_stdout_activations += 1

        bytes_since_checking_other_stream = 0
        while (stderr_content := process.stderr.read()) and (
            bytes_since_checking_other_stream < MAX_READ_SIZE_BYTES
        ):
            _write_to_stream(
                RED.encode() + stderr_content + RESET.encode(),
                "stderr",
            )
            len_stderr_content = len(stderr_content)
            bytes_since_checking_other_stream += len_stderr_content
            total_stderr_bytes += len_stderr_content
        if bytes_since_checking_other_stream:
            total_stderr_activations += 1

        if (return_code := process.poll()) is not None:
            if enable_byte_count_log_at_end:
                print(
                    "==== color_stream statistics (approx.) ====",
                    file=sys.stderr,
                )
                print(
                    f"Total stdout bytes: {total_stdout_bytes:,}",
                    file=sys.stderr,
                )
                print(
                    (
                        "Total stdout activations: "
                        f"{total_stdout_activations:,}"
                    ),
                    file=sys.stderr,
                )
                print(
                    f"Total stderr bytes: {total_stderr_bytes:,}",
                    file=sys.stderr,
                )
                print(
                    (
                        "Total stderr activations: "
                        f"{total_stderr_activations:,}"
                    ),
                    file=sys.stderr,
                )

            sys.exit(return_code)


def main() -> None:
    """Run the main entry point."""
    usage_str = "Usage: python -m color_stream [optional: --stat] '<command>'"

    if len(sys.argv) <= 1:
        print(usage_str)
        sys.exit(1)

    elif len(sys.argv) == 2:
        if sys.argv[1] in ("-h", "--help"):
            print(usage_str)
            sys.exit(0)
        elif sys.argv[1] in ("-v", "--version"):
            print(f"color_stream {__version__}")
            sys.exit(0)

    if sys.argv[1] in ("--stat", "--stats"):
        enable_byte_count_log_at_end = True
        command_parts = sys.argv[2:]
    else:
        enable_byte_count_log_at_end = False
        command_parts = sys.argv[1:]

    # Join the command arguments.
    command = " ".join(command_parts)
    run_command_with_colored_streams(
        command,
        enable_byte_count_log_at_end=enable_byte_count_log_at_end,
    )


if __name__ == "__main__":
    main()
