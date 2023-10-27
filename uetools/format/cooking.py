import logging

from uetools.format.base import Formatter, colored, colors, short

log = logging.getLogger()


class CookingFormatter(Formatter):
    """Makes the cooking summary more readable"""

    def __init__(self, col=None) -> None:
        super().__init__(col)
        self.summary_starts = 0
        self.print_non_matching = True

    # pylint: disable=too-many-arguments,unused-argument
    def default_format(self, datetime=None, frame=None, category=None, verbosity=None, message=None):
        """Formattings for the default log format"""
        verb = short.get(verbosity, " ")

        if verb == " ":
            log.debug("%s", verbosity)

        category = f"{{:<{self.longest_category}}}".format(category)

        color = colors.get(verb)

        self.print(f"[{verb}][{category}] {colored(message, color=color)}")

    # pylint: disable=too-many-arguments
    def format(self, datetime=None, frame=None, category=None, verbosity=None, message=None):
        if "Warning/Error Summary (Unique only)" in message:
            self.summary_starts += 1
            self.default_format(datetime, frame, category, verbosity, message)
            return

        if "-----------------------------------" in message:
            self.summary_starts += 1
            self.default_format(datetime, frame, category, verbosity, message)
            return

        if message == 0:
            self.summary_starts = 0

        if self.summary_starts == 2:
            self.default_format(datetime, frame, category, verbosity, "> " + message)
            return

        self.default_format(datetime, frame, category, verbosity, message)
