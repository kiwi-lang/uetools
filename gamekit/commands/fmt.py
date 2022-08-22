import os
import sys
import re
import logging
from collections import defaultdict
import subprocess

import colorama
from colorama import Style, Fore, Back

from gamekit.conf import WINDOWS
from gamekit.conf import load_conf, Command, update_conf, LINUX


log = logging.getLogger()

UE_LOG_FORMAT = re.compile('^(\[(?P<datetime>.*)\]\[\s*(?P<frame>\d*)\])?(?P<category>[A-Za-z]*): ((?P<verbosity>[A-Za-z]*):)?(?P<message>.*)')

UE_LOG_FORMAT_UTC = re.compile('^\[(?P<datetime>\d{4}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}:\d{3})\]\[\s*(?P<frame>\d*)\](?P<category>[A-Za-z]*): ((?P<verbosity>[A-Za-z]*):)?(?P<message>.*)')

UE_STDOUT_FORMAT = re.compile('^(?P<category>[A-Za-z]*): ((?P<verbosity>[A-Za-z]*):)?(?P<message>.*)')

log_verbosity = [
    'Fatal',
    'Error',
    'Warning',
    'Display',
    'Log',
    'Verbose',
    'VeryVerbose'
]

bad_logs = ['Fatal', 'Error', 'Warning']

short = dict(
    Fatal='F',
    Error='E',
    Warning='W',
    Display='D',
    Log='L',
    Verbose='V',
    VeryVerbose='T',
)


colors = dict(
    F='red',
    E='red',
    W='yellow',
)


COLORAMA = {
    'red': Fore.RED,
    'blue': Fore.BLUE,
    'green': Fore.GREEN,
    'yellow': Fore.YELLOW,
}


def colored(text, color, attrs=None):

    if color is None:
        return text

    return COLORAMA[color.lower()] + text + Style.RESET_ALL


# The loggging format is specfiied in the follorwing function calls
# Logf_InternalImpl(File, Line, Category, Verbosity, Fmt, Args...);
# FPlatformMisc::LowLevelOutputDebugStringf(TEXT("%s%s"),*FOutputDeviceHelper::FormatLogLine(Verbosity, Category, Data, GPrintLogTimes, Time),LINE_TERMINATOR);

class Formater:
    def __init__(self, col=None) -> None:
        # This is needed for windows
        colorama.init()

        self.col = col
        self.longest_category = load_conf().get('longest_category', 0)
        self.longest_name = load_conf().get('longest_name', '')
        self.regex = UE_LOG_FORMAT
        self.print_non_matching= False
        self.bad_logs = []

        if self.col is not None:
            self.longest_category = self.col

    def _meta(self, category):
        if self.col is not None:
            return

        self.longest_category = max(self.longest_category, len(category))
        self.longest_name = category if len(category) > len(self.longest_name) else self.longest_name

    def summary(self):
        print('-' * 80)
        print('    Summary')
        print('=' * 80)
        for line in self.bad_logs:
            print('  - ', end='')
            Formater.format(self, **line)
        print('=' * 80)

    def __del__(self):
        update_conf(longest_category=self.longest_category)

    def match_regex(self, line):
        result = self.regex.search(line)

        if result:
            data = result.groupdict()

            if data['verbosity'] is None:
                data['verbosity'] = 'Log'

            if data['verbosity'] not in log_verbosity:
                msg = data['verbosity']
                data['verbosity'] = 'Log'
                data['message'] = f'{msg}: ' + data['message']

            # Kepp track of bad logs and show a summary at the end
            if data['verbosity'] in bad_logs:
                self.bad_logs.append(data)

            self.format(**data)
        else:
            if self.print_non_matching:
                print(line, end='')
            else:
                log.debug('    Line did not match anything')
                log.debug('        - `%s`', line)


    def format(self, datetime=None, frame=None, category=None, verbosity=None, message=None):
        """

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
        self._meta(category)
        s = short.get(verbosity, ' ')

        if s == ' ':
            log.debug('%s', verbosity)

        category = f'{{:<{self.longest_category}}}'.format(category)

        color = colors.get(s)

        if frame is None:
            frame = 0

        print(f'[{int(frame):3d}][{s}][{category}] {colored(message, color=color)}')


class CookingFormater(Formater):
    def __init__(self, col=None) -> None:
        super().__init__(col)
        self.regex = UE_LOG_FORMAT
        self.summary_starts = 0
        self.print_non_matching = True

    def default_format(self, datetime=None, frame=None, category=None, verbosity=None, message=None):
        s = short.get(verbosity, ' ')

        if s == ' ':
            log.debug('%s', verbosity)

        category = f'{{:<{self.longest_category}}}'.format(category)

        color = colors.get(s)

        print(f'[{s}][{category}] {colored(message, color=color)}')

    def format(self, datetime=None, frame=None, category=None, verbosity=None, message=None):
        if 'Warning/Error Summary (Unique only)' in message:
            self.summary_starts += 1
            self.default_format(datetime, frame, category, verbosity, message)
            return

        if '-----------------------------------' in message:
            self.summary_starts += 1
            self.default_format(datetime, frame, category, verbosity, message)
            return

        if message == 0:
            self.summary_starts = 0

        if self.summary_starts == 2:
            self.default_format(datetime, frame, category, verbosity, '> ' + message)
            return

        self.default_format(datetime, frame, category, verbosity, message)


class TestFormater(Formater):
    def __init__(self, col=None) -> None:
        super().__init__(col)
        self.indent = 0
        self.allow_everything = False
        self.iterating_overlist = False

    def default_format(self, *args, **kwargs):
        Formater.format(self, *args, **kwargs)

    def format(self, datetime=None, frame=None, category=None, verbosity=None, message=None):
        valid_line = 'Automation' in category or 'Python' in category or self.allow_everything

        if not valid_line:
            self.default_format(datetime, frame, category, verbosity, message)
            return

        # ------------
        # Testing init
        # ------------
        if 'automation tests based on' in message:
            self.iterating_overlist = True
            self.default_format(datetime, frame, category, verbosity, '- ' + message)
            return

        # This is only printed in logs
        if 'Sending StopTests' in message:
            self.iterating_overlist = False
            self.default_format(datetime, frame, category, verbosity, message)
            return

        # -----
        # Tests
        # -----
        if 'Test Started' in message:
            message = '>' + colored(message, 'blue', attrs=['bold'])
            self.indent += 4
            self.iterating_overlist = False
            self.allow_everything = True
            self.default_format(datetime, frame, category, verbosity, message)
            return

        if 'Test Completed' in message:
            self.indent -= 4
            self.allow_everything = False

            if 'Success' in message:
                message = '<' + colored(message, 'green')
            else:
                message = '<' + colored(message, 'red')

            self.default_format(datetime, frame, category, verbosity, message)
            return

        if 'BeginEvents' in message:
            self.indent += 4
            self.allow_everything = True
            self.default_format(datetime, frame, category, verbosity, '+ ' + message)
            return

        if 'EndEvents' in message:
            self.indent -= 4
            self.allow_everything = False
            self.default_format(datetime, frame, category, verbosity, '- ' + message)
            self.default_format(datetime, frame, category, verbosity, '')
            return

        if self.iterating_overlist:
            self.default_format(datetime, frame, category, verbosity, '    * ' + message.strip())
            return


        message = ' ' * self.indent + message.strip()
        self.default_format(datetime, frame, category, verbosity, message)


profiles = dict(
    test=TestFormater,
    cook=CookingFormater
)

class Format(Command):
    """Format UnrealEngine log output"""

    name: str = "format"

    @staticmethod
    def arguments(subparsers):
        fmt = subparsers.add_parser(
            Format.name, help="Format UnrealEngine logs"
        )
        fmt.add_argument('--file', default=None, type=str, help='path to a log file')
        fmt.add_argument('--profile', default=None, type=str, help='formating profile')
        fmt.add_argument('--fail-on-error', default=False, action='store_true', help='formating profile')
        # 24 was chosen because it is 90% of the time longer than the category name
        # Picking the biggest number just takes too much space
        fmt.add_argument('--col', default=24, type=int, help='size of the category column')

    def __init__(self, profile=None):
        self.profile = profile

    @staticmethod
    def execute(args):
        colorama.init()

        fmt = profiles.get(args.profile, Formater)(args.col)

        if args.file is not None:
            with open(args.file, 'r') as file:
                for line in file:
                    fmt.match_regex(line)
            return

        for line in sys.stdin:
            fmt.match_regex(line)

        print('-' * 80)
        print('    Summary')
        print('=' * 80)
        for line in fmt.bad_logs:
            print('  - ', end='')
            Formater.format(fmt, **line)
        print('=' * 80)

        if args.fail_on_error and len(fmt.bad_logs) > 0:
            sys.exit(1)


logging.basicConfig(level=logging.CRITICAL)

COMMAND = Format


def popen_with_format(fmt, args):
    p = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        # This is needed because without lines might not be recognized as such
        text=True,
    )

    while p.poll() is None:
        # sys.stdout.flush()

        line = p.stdout.readline()

        if len(line) > 0:
            fmt.match_regex(line)

    return p.poll()
