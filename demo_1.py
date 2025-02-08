#!/usr/bin/env python3

"""A demonstration script to show how `color_stream` works.

Call like: `python3 -m color_stream 'python3 demo_1.py'`
"""

import json
import random
import sys
import time
from typing import Literal

stream_stats = {
    "stdout": {"bytes": 0, "activations": 0},
    "stderr": {"bytes": 0, "activations": 0},
}


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

    # Update the stream stats.
    stream_stats[stream]["bytes"] += len(message) + len(end)
    stream_stats[stream]["activations"] += 1

    stream_id.write(message)
    stream_id.write(end)
    stream_id.flush()


def main_1() -> None:
    """Print various stdout and stderr messages."""
    print_to_stream("Hello, stdout", stream="stdout")
    print_to_stream("Hello, stderr", stream="stderr")
    time.sleep(1)

    for i in range(5):
        print_to_stream(f"Counting {i} stdout...", stream="stdout", end=" ")
        print_to_stream(f"Counting {i} stderr...", stream="stderr", end=" ")
        time.sleep(0.5)
    print_to_stream("Done counting!", "stdout")

    print_to_stream(
        "\n\n==== Starting random stdout/stderr, 500ms delay ====",
        stream="stdout",
    )
    for i in range(5):
        f = random.choice(["stdout", "stderr"])  # noqa: S311
        print_to_stream(f"Counting {i} onto {f}...", stream=f, end=" ")
        time.sleep(0.5)

    print_to_stream(
        "\n\n==== Starting alternating stdout/stderr, 10ms delay ====",
        stream="stdout",
    )
    for i in range(10):
        f = "stdout" if i % 2 == 0 else "stderr"
        print_to_stream(f"Counting {i} onto {f}...", stream=f, end=" ")
        time.sleep(0.01)

    print_to_stream(
        "\n\n==== Starting all done messages... ====",
        stream="stdout",
    )
    print_to_stream("All done (stderr)!", stream="stderr")
    print_to_stream("All done (stdout)!", stream="stdout")

    stats_json = json.dumps(stream_stats, indent=4)
    print_to_stream(
        f"\n\n==== From inside '{__file__}', dump stats... ====\n{stats_json}",
        stream="stderr",
    )

    # Stats notes: The channel that the stats are printed to will show a way
    # higher byte count in the `color_stream` output, because those stats will
    # include the bytes used to print the stats themselves.


if __name__ == "__main__":
    main_1()
