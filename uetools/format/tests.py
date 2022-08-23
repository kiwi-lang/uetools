from uetools.format.base import Formatter, colored


class TestFormatter(Formatter):
    """Format test output to be more readable"""

    def __init__(self, col=None) -> None:
        super().__init__(col)
        self.indent = 0
        self.allow_everything = False
        self.iterating_overlist = False

    def default_format(self, *args, **kwargs):
        """Default format function"""
        Formatter.format(self, *args, **kwargs)

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-return-statements
    def format(
        self, datetime=None, frame=None, category=None, verbosity=None, message=None
    ):
        """Format test output to be more readable"""
        valid_line = (
            "Automation" in category or "Python" in category or self.allow_everything
        )

        if not valid_line:
            self.default_format(datetime, frame, category, verbosity, message)
            return

        # ------------
        # Testing init
        # ------------
        if "automation tests based on" in message:
            self.iterating_overlist = True
            self.default_format(datetime, frame, category, verbosity, "- " + message)
            return

        # This is only printed in logs
        if "Sending StopTests" in message:
            self.iterating_overlist = False
            self.default_format(datetime, frame, category, verbosity, message)
            return

        # -----
        # Tests
        # -----
        if "Test Started" in message:
            message = ">" + colored(message, "blue", attrs=["bold"])
            self.indent += 4
            self.iterating_overlist = False
            self.allow_everything = True
            self.default_format(datetime, frame, category, verbosity, message)
            return

        if "Test Completed" in message:
            self.indent -= 4
            self.allow_everything = False

            if "Success" in message:
                message = "<" + colored(message, "green")
            else:
                message = "<" + colored(message, "red")

            self.default_format(datetime, frame, category, verbosity, message)
            return

        if "BeginEvents" in message:
            self.indent += 4
            self.allow_everything = True
            self.default_format(datetime, frame, category, verbosity, "+ " + message)
            return

        if "EndEvents" in message:
            self.indent -= 4
            self.allow_everything = False
            self.default_format(datetime, frame, category, verbosity, "- " + message)
            self.default_format(datetime, frame, category, verbosity, "")
            return

        if self.iterating_overlist:
            self.default_format(
                datetime, frame, category, verbosity, "    * " + message.strip()
            )
            return

        message = " " * self.indent + message.strip()
        self.default_format(datetime, frame, category, verbosity, message)
