"""A demonstration script to show how `color_stream` works.

Call like: `python3 -m color_stream 'python3 demo_1.py'`
"""

import random
import sys
import time
from typing import Literal


def print_to_stream(
    message: str, stream: Literal["stdout", "stderr"], end: str = "\n"
) -> None:
    """Print output to either stdout or stderr."""
    if stream == "stdout":
        stream_id = sys.stdout
    elif stream == "stderr":
        stream_id = sys.stderr
    else:
        msg = f"Invalid stream: {stream}"
        raise ValueError(msg)

    stream_id.write(message)
    stream_id.write(end)
    stream_id.flush()


def main_1() -> None:
    """Print various stdout and stderr messages."""
    print_to_stream("Hello, stdout", "stdout")
    print_to_stream("Hello, stderr", "stderr")
    time.sleep(1)

    for i in range(5):
        print_to_stream(f"Counting {i} stdout...", "stdout", end=" ")
        print_to_stream(f"Counting {i} stderr...", "stderr", end=" ")
        time.sleep(0.5)
    print_to_stream("Done counting!", "stdout")

    for i in range(5):
        f = random.choice(["stdout", "stderr"])  # noqa: S311
        print_to_stream(f"Counting {i} onto {f}...", "stderr", end=" ")
        time.sleep(0.5)

    print_to_stream("All done!", "stderr")
    print_to_stream("All done!", "stdout")


if __name__ == "__main__":
    main_1()
