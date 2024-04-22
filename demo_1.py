#!/usr/bin/env python3

import sys
import time
import random
from typing import Literal

# This script a demonstration to show how split_colors.py works.


def print_to_stream(
    message, stream: Literal["stdout", "stderr"], end: str = "\n"
) -> None:
    if stream == "stdout":
        # print(message, file=sys.stdout, end=end)
        stream_id = sys.stdout
    elif stream == "stderr":
        # print(message, file=sys.stderr, end=end)
        stream_id = sys.stderr
    else:
        raise ValueError(f"Invalid stream: {stream}")

    stream_id.write(message)
    stream_id.write(end)
    stream_id.flush()


def main_1() -> None:
    print_to_stream("Hello, stdout", "stdout")
    print_to_stream("Hello, stderr", "stderr")
    time.sleep(1)

    for i in range(5):
        print_to_stream(f"Counting {i} stdout...", "stdout", end=" ")
        print_to_stream(f"Counting {i} stderr...", "stderr", end=" ")
        time.sleep(0.5)
    print_to_stream("Done counting!", "stdout")

    for i in range(5):
        f = random.choice(["stdout", "stderr"])
        print_to_stream(f"Counting {i} onto {f}...", "stderr", end=" ")
        time.sleep(0.5)

    print_to_stream("All done!", "stderr")
    print_to_stream("All done!", "stdout")


if __name__ == "__main__":
    main_1()
