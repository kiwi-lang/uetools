f = "ubt_xml.html"

with open("ubt_xml.html") as file:
    lines = file.readlines()


from collections import defaultdict

data = defaultdict()
current = None
attr = None


def parse(line):
    # Note this only works if we have a single tag per line
    global data, current, attr

    if line == "":
        return 0

    if line.startswith("<div"):
        return 0

    if line.startswith("<h3"):
        s = line.find(">")
        e = line.rfind("<")

        name = line[s + 1 : e]
        obj = dict()
        data[name] = obj
        current = obj
        return 1

    if line.startswith("<dl"):
        return 2

    if line.startswith("<dt"):
        s = line.find(">")
        e = line.rfind("<")
        attr = line[s + 1 : e].strip()
        current[attr] = None
        return 3

    if line.startswith("<dd"):
        return 4

    if line.startswith("<p"):
        s = line.find(">")
        e = line.rfind("<")
        comment = line[s + 1 : e]
        current[attr] = comment
        return 5

    if line.startswith("</dd"):
        attr = None
        return 6

    if line.startswith("</dl"):
        return 7

    if line.startswith("</div"):
        return 0

    print(line)


for line in lines:
    v = parse(line.strip())


for k, v in data.items():
    print("@dataclass")
    print(f"class {k}T:")
    for k, v in v.items():
        type = "bool" if k[0] == "b" else "str"
        print(f"    {k:<30}: {type:<5} = None  #  {v}")
    print()
    print()


print("@dataclass")
print("class Configuration:")

for k, v in data.items():
    t = f"{k}T"
    print(f"    {k:<30}: {t:<30} = field(default_factory={k}T)")
