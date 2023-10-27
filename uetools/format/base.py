import logging
import re

import colorama
from colorama import Fore, Style

from uetools.core.conf import load_conf, update_conf

log = logging.getLogger()

UE_LOG_FORMAT = re.compile(r"^(\[(?P<datetime>.*)\]\[\s*(?P<frame>\d*)\])?(?P<category>[A-Za-z]*): ((?P<verbosity>[A-Za-z]*):)?(?P<message>.*)")

UE_LOG_FORMAT_UTC = re.compile(r"^\[(?P<datetime>\d{4}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}:\d{3})\]\[\s*(?P<frame>\d*)\](?P<category>[A-Za-z]*): ((?P<verbosity>[A-Za-z]*):)?(?P<message>.*)")
UE_STDOUT_FORMAT = re.compile(r"^(?P<category>[A-Za-z]*): ((?P<verbosity>[A-Za-z]*):)?(?P<message>.*)")

UAT_ERROR_1 = re.compile(r"^RunUAT ERROR: AutomationTool was unable to run successfully. Exited with code: (?P<returncode>[0-9]*)")
UAT_ERROR_2 = re.compile(r"^AutomationTool exiting with ExitCode=(?P<returncode>[0-9]*) \((?P<message>[a-zA-Z0-9]*)\)")

ERROR_PATERNS = [
    UAT_ERROR_1,
    UAT_ERROR_2,
]

log_verbosity = [
    "Fatal",
    "Error",
    "Warning",
    "Display",
    "Log",
    "Verbose",
    "VeryVerbose",
]

bad_logs = ["Fatal", "Error", "Warning"]

short = dict(
    Fatal="F",
    Error="E",
    Warning="W",
    Display="D",
    Log="L",
    Verbose="V",
    VeryVerbose="T",
)


colors = dict(
    F="red",
    E="red",
    W="yellow",
)


COLORAMA = {
    "red": Fore.RED,
    "blue": Fore.BLUE,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
}


# pylint: disable=unused-argument
def colored(text, color, attrs=None):
    """Returns a colored text"""
    if color is None:
        return text

    return COLORAMA[color.lower()] + text + Style.RESET_ALL


# The logging format is specified in the follorwing function calls
# Logf_InternalImpl(File, Line, Category, Verbosity, Fmt, Args...);
# FPlatformMisc::LowLevelOutputDebugStringf(TEXT("%s%s"),
#   *FOutputDeviceHelper::FormatLogLine(Verbosity, Category, Data, GPrintLogTimes, Time),LINE_TERMINATOR);
#


class Formatter:
    """Parse an unreal engine output log line and formats it"""

    def __init__(self, col=None) -> None:
        # This is needed for windows
        colorama.init()

        self.col = col
        self.longest_category = load_conf().get("longest_category", 0)
        self.longest_name = load_conf().get("longest_name", "")
        self.regex = UE_LOG_FORMAT
        self.print_non_matching = False
        self.bad_logs = []
        self.ignore = set()
        self.only = set()
        self.return_codes = []
        self.print = print

        if self.col is not None:
            self.longest_category = self.col

    def _meta(self, category):
        if self.col is not None:
            return

        self.longest_category = max(self.longest_category, len(category))
        self.longest_name = category if len(category) > len(self.longest_name) else self.longest_name

    def summary(self):
        """Print a summary of warnings and errors that got parsed during the formatting process"""
        self.print("-" * 80)
        self.print("    Summary")
        self.print("=" * 80)
        for line in self.bad_logs:
            self.print("  - ", end="")
            Formatter.format(self, **line)
        self.print("=" * 80)

    def __del__(self):
        update_conf(longest_category=self.longest_category)

    def match_regex(self, line):
        """Parse a log line using regex"""
        result = self.regex.search(line)

        if result:
            data = result.groupdict()

            if data["verbosity"] is None:
                data["verbosity"] = "Log"

            if data["verbosity"] not in log_verbosity:
                msg = data["verbosity"]
                data["verbosity"] = "Log"
                data["message"] = f"{msg}: " + data["message"]

            # Kepp track of bad logs and show a summary at the end
            if data["verbosity"] in bad_logs:
                self.bad_logs.append(data)

            self.format(**data)
        else:
            if self.print_non_matching:
                self.print(line, end="")
            else:
                log.debug("    Line did not match anything")
                log.debug("        - `%s`", line)

        # Error detection
        for error_pat in ERROR_PATERNS:
            result = error_pat.search(line)

            if result:
                data = result.groupdict()

                rc = data.get("returncode", 0)
                if rc != 0:
                    self.return_codes.append(int(rc))

    def returncode(self):
        if self.return_codes:
            return self.return_codes[0]
        return 0

    # pylint: disable=too-many-arguments
    def format(self, datetime=None, frame=None, category=None, verbosity=None, message=None):
        """Creates column for each element of the log and print the message last.

        Parameters
        ----------

        datetime:
            Can be, UTC, local, seconds since start or time code (Frametime converted)

        frame:
            GFrameCounter % 1000

        category:
            log category

        verbosity:
            log verbosity

        message:
            log message

        """
        if category in self.ignore:
            return

        if len(self.only) > 0 and category not in self.only:
            return

        self._meta(category)
        verb = short.get(verbosity, " ")

        if verb == " ":
            log.debug("%s", verbosity)

        category = f"{{:<{self.longest_category}}}".format(category)

        color = colors.get(verb)

        if frame is None:
            frame = 0

        self.print(f"[{int(frame):3d}][{verb}][{category}] {colored(message, color=color)}")
