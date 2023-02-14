import subprocess

# This is a bit of future proofing in case I start to need to wrap it
run = subprocess.run


def popen_with_format(fmt, args, shell=False):
    """Execute a command with the given formatter."""
    with subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        # This is needed because without lines might not be recognized as such
        text=True,
        shell=shell,
    ) as process:
        try:
            while process.poll() is None:
                # sys.stdout.flush()

                line = process.stdout.readline()

                if len(line) > 0:
                    fmt.match_regex(line)

            return process.poll() + fmt.returncode()
        except KeyboardInterrupt:
            print("Stopping due to user interrupt")
            process.kill()

        return -1
