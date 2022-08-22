
import subprocess
import tempfile


def change_letter(svg, c):
    return svg.replace('>A</tspan></text>', f'>{c}</tspan></text>')

def svg_to_png(svgfile: str, outputpath: str, dpi: int = 96):
    INKSPACE = 'C:/Users/Newton/Downloads/inkscape-1.2_2022-05-15_dc2aedaf03-x64/bin/inkscape.exe'

    out = subprocess.run([
            INKSPACE,
            '-o', outputpath,
            '-d', str(dpi),
            svgfile
        ],
        capture_output=True,
    )

    if out.returncode != 0:
        print(out.stderr.decode('utf-8'))
        print(out.stdout.decode('utf-8'))


def generate_keyboard_icons():
    PATH = 'E:/GameAssets'
    TEMPLATE = f'{PATH}/Key_A.svg'
    OUT = 'E:/GameAssets/'

    chars = [
        ('espace', '⎋'),
        ('tab', '⇥'),
        ('capslock', '🔒')
        # ('capslock', '⇪'),
        ('shift', '⇧'),
        ('ctrl', 'ctrl'),
        ('space', '␣'),
        ('return', '⏎'),
        ('backspace', '⌫'),
        ('delete1', '⌦'),
        ('up', '↑'),
        ('down', '↓'),
        ('left', '←'),
        ('right', '→'),
        ('c', 'c'),
        ('w', 'w'),
        ('a', 'a'),
        ('s', 's'),
        ('d', 'd'),
        ('i', 'i'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('1', '1'),
    ]

    with open(TEMPLATE, 'r') as file:
        svgtemplate = file.read()

    for name, c in chars:
        print(name)
        with tempfile.NamedTemporaryFile() as file:
            file.write(change_letter(svgtemplate, c).encode('utf-8'))
            file.flush()

            svg_to_png(file.name, f'{OUT}/Generated/KeyboardIcon_{name}.png')

    custom_files = [
        'Key_Backspace.svg',
        'Key_Space.svg',
        'Key_Ctrl.svg',
        'Key_Enter.svg',
        'Key_Shift.svg',
    ]

    for filename in custom_files:
        name = filename.split('_')[-1]
        name = name.split('.')[0]

        svg_to_png(f'{PATH}/{filename}', f'{OUT}/Generated/KeyboardIcon_{name}.png')
