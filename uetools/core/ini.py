import io
import re
from collections import defaultdict
from dataclasses import dataclass

SECTION_REGEX = re.compile(r"\[(?P<section>.*)\]")
KEY_REGEX = re.compile(r"(?P<op>(\+|-|\.|!))?(?P<key>.*)=(?P<value>.*)")
COMMENT_REGEX = re.compile(r";(?P<comment>.*)")


# pylint: disable=too-few-public-methods
class Entry:
    """Base Entry of the INI AST"""


KEY = ""
ADD = "+"
REM = "-"
ADD_PROPERTY = "."
REM_PROPERTY = "!"


@dataclass
class Section(Entry):
    """Section inside an ini file"""

    title: str

    def to_ini(self):
        """Convert the entry to a ini line"""
        return f"[{self.title}]\n"


@dataclass
class Key(Entry):
    """Key value inside an ini file"""

    op: str
    key: str
    value: str

    def to_ini(self):
        """Convert the entry to a ini line"""
        return f"{self.op}{self.key}={self.value}\n"


@dataclass
class Comment(Entry):
    """Comment inside an ini file"""

    comment: str

    def to_ini(self):
        """Convert the entry to a ini line"""
        return f";{self.comment}\n"


@dataclass
class Newline(Entry):
    """New line inside an ini file"""

    def to_ini(self):
        """Convert the entry to a ini line"""
        return "\n"


def fake_config_file():
    """Testing config"""
    return io.StringIO(
        """
[/Script/Section]
+Weird.Key1=(Name="Q",Command="Foo")
-Weird/Key2=(OldClassName="TP_BlankGameModeBase",NewClassName="GamekitDevGameModeBase")
.Weird,Key3=1
!Weird*Key4=True

[Another.Section]
UniqueKey=123

"""
    )


class UnrealINIParser:
    """Parse a Unreal INI configuration file
    It tries to minimize the number of modification it makes when updating
    the configuration file

    Examples
    --------

    >>> ini = UnrealINIParser(fake_config_file())
    >>> ini.insert('Another.Section', 'UniqueKey', 3)
    'updated'

    >>> file = io.StringIO()
    >>> ini.write(file)
    >>> print(file.getvalue())
    <BLANKLINE>
    [/Script/Section]
    +Weird.Key1=(Name="Q",Command="Foo")
    -Weird/Key2=(OldClassName="TP_BlankGameModeBase",NewClassName="GamekitDevGameModeBase")
    .Weird,Key3=1
    !Weird*Key4=True
    <BLANKLINE>
    [Another.Section]
    UniqueKey=3
    <BLANKLINE>
    <BLANKLINE>

    >>> ini.remove('Another.Section', 'UniqueKey')
    'removed'

    >>> file = io.StringIO()
    >>> ini.write(file)
    >>> print(file.getvalue())
    <BLANKLINE>
    [/Script/Section]
    +Weird.Key1=(Name="Q",Command="Foo")
    -Weird/Key2=(OldClassName="TP_BlankGameModeBase",NewClassName="GamekitDevGameModeBase")
    .Weird,Key3=1
    !Weird*Key4=True
    <BLANKLINE>
    [Another.Section]
    <BLANKLINE>
    <BLANKLINE>

    >>> ini.insert('New.Section', 'UniqueKey1', 123)
    'inserted'

    >>> ini.insert('New.Section', 'UniqueKey2', 123)
    'inserted'

    >>> ini.insert('New.Section', 'UniqueKey2', 4)
    'updated'


    >>> file = io.StringIO()
    >>> ini.write(file)
    >>> print(file.getvalue())
    <BLANKLINE>
    [/Script/Section]
    +Weird.Key1=(Name="Q",Command="Foo")
    -Weird/Key2=(OldClassName="TP_BlankGameModeBase",NewClassName="GamekitDevGameModeBase")
    .Weird,Key3=1
    !Weird*Key4=True
    <BLANKLINE>
    [Another.Section]
    <BLANKLINE>
    [New.Section]
    UniqueKey1=123
    UniqueKey2=4
    <BLANKLINE>

    """

    def __init__(self, fp) -> None:
        # Main references: keeps the file order stable
        # to minimise diffs on updates
        self.sections = [None]

        # Index
        self.entries = defaultdict(list)
        self.entries[None] = []

        # for unique section, key pairs
        self.entries_key = defaultdict(list)

        # Parsing state
        self.current_section = None

        self.parse_file(fp)

    def insert(self, section, key, value, op=KEY):
        """Insert or update a new key"""
        if op == KEY:
            # Change the value of an existing entry
            if (section, key) in self.entries_key:
                entry = self.entries_key[(section, key)][0]
                entry.value = value
                return "updated"

            # add a new entry to the section
            entries = self.entries.get(section, None)

            if entries is None:
                entry = Section(section)
                self.sections.append(entry)

                entries = self.entries[section]

            entry = Key(op, key, value)
            entries.append(entry)

            self.entries_key[(section, key)].append(entry)
            return "inserted"

        # we do not need the functionality right now
        raise NotImplementedError()

    def remove(self, section, key, op=KEY):
        """Remove a key"""
        if op == KEY:
            # Change the value of an existing entry
            if (section, key) in self.entries_key:
                entry = self.entries_key.pop((section, key))[0]

                entries = self.entries[section]
                entries.remove(entry)
                return "removed"

            return "missing"

        # we do not need the functionality right now
        raise NotImplementedError()

    def write(self, fp):
        """Write the current configuration to a file"""
        for section in self.sections:
            if section:
                fp.write(section.to_ini())

            title = section.title if section else None
            entries = self.entries[title]

            for entry in entries:
                fp.write(entry.to_ini())

    def parse_file(self, fp):
        """Parse a file"""
        for line in fp.readlines():
            self.parse_line(line)

    def parse_line(self, line):
        """Parse a line"""
        line = line.strip()

        if line == "":
            self.entries[self.current_section].append(Newline())
            return

        result = KEY_REGEX.search(line)
        if result:
            self.process_key(**result.groupdict())
            return

        result = SECTION_REGEX.search(line)
        if result:
            self.process_section(**result.groupdict())
            return

        result = COMMENT_REGEX.search(line)
        if result:
            self.process_comment(**result.groupdict())
            return

    def process_key(self, op, key, value):
        """Parse a key"""
        assert key is not None
        assert self.current_section is not None
        if op is None:
            op = KEY

        entry = Key(op, key, value)

        self.entries[self.current_section].append(entry)
        self.entries_key[(self.current_section, key)].append(entry)

    def process_section(self, section):
        """Parse a section"""
        entry = Section(section)

        self.sections.append(entry)
        self.current_section = section

    def process_comment(self, comment):
        """Parse a comment"""
        entry = Section(comment)
        self.entries[self.current_section].append(entry)
