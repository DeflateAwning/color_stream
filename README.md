# color_stream
A quick Python script to run another shell command, and split/color the
stdout/stderr streams green/red

## Story

While working with redirecting and assessing the output from another CLI tool,
I needed a way to see what was going to stderr, and what was going to stdout.

This tool highlights the two streams, in real time.

## Usage

```bash
pip install color_stream

color_stream '<another command here>'
## OR ##
python3 -m color_stream '<another command here>'

# test it with the demo script in this repo
color_stream python demo_1.py

# test it with "ls" (success, and error with file that doesn't exist)
color_stream ls file_that_exists.txt file_that_does_not_exist.txt
```

## Limitations

- [ ] reading from stdin is untested, and likely doesn't work
- [ ] throughput speed is currently not benchmarked
- [ ] switching colors is not currently supported
