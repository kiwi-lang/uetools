from dataclasses import dataclass
import inspect
import re


@dataclass
class SourceCursor:
    i: int = 0

docstring_oneline = re.compile(r'(\s*)"""(.*)"""')
docstring_start = re.compile(r'(\s*)"""(.*)')
docstring_end = re.compile(r'(.*)"""')

class DocstringIterator:
    """Looks for docstring included inherited fields"""
    def __init__(self, dataclass) -> None:
        parents = dataclass.__mro__
        self.classes = parents[:-1]

        self.cursors = []
        self.sources = []
        for cls in self.classes:
            self.cursors.append(SourceCursor())
            self.sources.append(
                inspect.getsource(cls).splitlines()
            )

    def get_dataclass_docstring(self):
        docstrings = []

        for source, cursor in zip(self.sources, self.cursors):
            recognized = 0
            started = False
            docstring_lines = []

            for i, line in enumerate(source):
                if "@dataclass" in line:
                    recognized += 1
                    continue

                if "class " in line:
                    recognized += 1
                    continue

                if recognized == 2 and not started and docstring_oneline.match(line):
                    docstring_lines.append(line.strip()[3:-3])
                    break

                if recognized == 2 and not started and docstring_start.match(line):
                    started = True
                    docstring_lines.append(line.strip()[3:])
                    continue

                if started and docstring_end.match(line):
                    docstring_lines.append(line.strip()[:-3])
                    started = False
                    break

                if started:
                    docstring_lines.append(line.strip())
            else:
                i = 0

            cursor.i = i
            if len(docstring_lines) > 0:
                docstrings.append("\n".join(docstring_lines))

        if len(docstrings) > 0:
            return docstrings[0]

        return ""
    
    def find_field(self, field):
        for source, cursor in zip(self.sources, self.cursors):
            start = cursor.i
            nlines = len(source)

            while start < nlines and field.name not in source[start]:
                start += 1

            # No found
            if start >= nlines:
                continue

            idx = source[start].find("#")

            # Found
            if idx > 0:
                docstring = source[start][idx + 1 :].strip()
                cursor.i = start
                return docstring
            
        return None
