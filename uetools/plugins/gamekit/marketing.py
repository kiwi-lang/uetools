import os
from dataclasses import dataclass
from typing import List

from uetools.args.cache import load_resource
from uetools.args.command import Command, ParentCommand


Image = None
ImageDraw = None
ImageFont = None
ImageOps = None


def load_PIL():
    global Image, ImageDraw, ImageFont, ImageOps

    import PIL

    Image = PIL.Image
    ImageDraw = PIL.ImageDraw
    ImageFont = PIL.ImageFont
    ImageOps = PIL.ImageOps


@dataclass
class Banner:
    name: str
    width: int
    height: int
    count: int = 1


@dataclass
class Platform:
    name: str
    banners: List[Banner]


@dataclass
class Padding:
    top: int
    bot: int
    left: int
    right: int


platforms = [
    Platform(
        "Marketplace",
        [
            Banner("Gallery", 1920, 1080, count=25),
            Banner("Thumbnail", 284, 284),
            Banner("Featured", 894, 488),
        ],
    ),
    Platform(
        "itch.io",
        [
            Banner("Cover", 630, 500),
            Banner("Screenshots", -1, -1, count=5),
        ],
    ),
    Platform(
        "youtube",
        [
            Banner("Picture", 98, 98),
            Banner("Banner", 2048, 1152),
            Banner("Thumbnail", 1280, 720),
        ],
    ),
    Platform(
        "Patron",
        [
            Banner("Cover", 1600, 400),
        ],
    ),
    Platform(
        "Twitter",
        [
            Banner("Cover", 1500, 500),
            Banner("Profile", 400, 400),
        ],
    ),
]


def _frame(img, border=5, color=(255, 255, 255, 255)):
    img = ImageOps.crop(img, border=5)
    img = ImageOps.expand(img, border=5, fill=(255, 255, 255, 255))
    return img


def frame_image(imgpath, border=5, color=(255, 255, 255, 255)):
    img = Image.open(imgpath)
    img = _frame(img, border, color)
    return img


def create_image(folder: str, platform: Platform, banner: Banner, default=(1920, 1080)):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{platform.name}_{banner.name}.png")

    if banner.width <= 0:
        banner.width = default[0]

    if banner.height <= 0:
        banner.height = default[1]

    img = Image.new("RGB", (banner.width, banner.height))
    img.save(filepath)


def create_banner_templates(folder):
    for platform in platforms:
        for banner in platform.banners:
            create_image(folder, platform, banner)


def get_font():
    filepath = load_resource(__name__, "resources/Roboto-Regular.ttf")
    return filepath


def resize_image(imgpath, size):
    """Resize the image without ratio change or crop"""
    img = Image.open(imgpath)
    w, h = img.width, img.height

    multiplier = min(size[0] / w, size[1] / h)

    bigger = img.resize((int(w * multiplier), int(h * multiplier)), Image.BICUBIC)
    final_img = Image.new("RGB", size)

    offset = (
        (final_img.width - bigger.width) // 2,
        (final_img.height - bigger.height) // 2,
    )
    final_img.paste(bigger, offset)
    final_img.save("test.png")


def make_mark(text, font_size):
    font_name = get_font()
    font_color = (255, 255, 255)
    background = (255, 191, 0, 255)
    pad = Padding(top=5, bot=5, left=5, right=32)

    font = ImageFont.truetype(font_name, font_size)
    tw, th = font.getsize(text)

    img = Image.new("RGBA", (tw * 2, tw * 2), color=background)
    draw = ImageDraw.Draw(img)

    draw.text((tw - tw / 2, tw * 2 - th - pad.bot), text, font_color, font=font)

    return img.rotate(-45, Image.BICUBIC, expand=1, fillcolor=(0, 0, 0, 0))


def write_text_image(imgpath, text, mark=None, mark_offset=(20, 20)):
    font_name = get_font()
    font_size = 32
    font_color = (255, 255, 255)
    background = (255, 191, 0)

    font = ImageFont.truetype(font_name, font_size)

    img = Image.open(imgpath).convert("RGBA")
    draw = ImageDraw.Draw(img)

    w, h = img.size
    tw, th = font.getsize(text)
    pad = Padding(top=5, bot=5, left=5, right=32)

    start = h - (th + pad.top + pad.bot)
    length = tw + pad.left + pad.right

    assert length < w, "Text is too long and/or too big"

    # fmt: off
    draw.polygon([
        (0                 , start),
        (length            , start),
        (length - pad.right, h),
        (0                 , h)
    ], fill=background)
    # fmt: on

    draw.text((pad.left, start + pad.top), text, font_color, font=font)

    if mark:
        mark = make_mark(mark, font_size=16)
        dest = (
            w - mark.width // 2 + mark_offset[0],
            0 - mark.height // 2 - mark_offset[1],
        )
        img.paste(mark, dest, mark)

    img.save("test.png")


def to_tuple(arg: str):
    return tuple(int(v) for v in arg.split(","))


#
# Commands
# ========


class TemplateImg(Command):
    """Generate a bunch of template images for marketing on different platforms"""

    name: str = "template"

    # fmt: off
    @dataclass
    class Arguments:
        folder  : str  # Output path or image path
    # fmt: on

    @staticmethod
    def execute(args):
        load_PIL()
        create_banner_templates(args.folder)
        return 0


class ResizeImg(Command):
    """Resise an image and keep the aspect ratio"""

    name: str = "resize"

    # fmt: off
    @dataclass
    class Arguments:
        folder  : str                           # Output path or image path
        size    : str   = "0,0"                 # image to resize the image too
    # fmt: on

    @staticmethod
    def execute(args):
        load_PIL()

        resize_image(args.folder, to_tuple(args.size))
        return 0


class ShowcasheImg(Command):
    """Insert text to an image"""

    name: str = "showcase"

    # fmt: off
    @dataclass
    class Arguments:
        folder  : str                           # Output path or image path
        color   : str   = "255,255,255,255"     # color
        text    : str   = None                  # Title of the show case image
        mark    : str   = None                  # Mark of the show case image
        offset  : str   = "10,10"               # Mark offset
    # fmt: on

    @staticmethod
    def execute(args):
        load_PIL()
        write_text_image(args.folder, args.text, args.mark, to_tuple(args.offset))
        return 0


class FrameImg(Command):
    """Add a frame around the image without changing its size"""

    name: str = "frame"

    # fmt: off
    @dataclass
    class Arguments:
        folder  : str                           # Output path or image path
        color   : str   = "255,255,255,255"     # color
        border  : int   = 5                     # Frame border
    # fmt: on

    @staticmethod
    def execute(args):
        load_PIL()
        color = to_tuple(args.color)
        border = args.border

        output = os.path.join(args.folder, "framed")
        os.makedirs(output, exist_ok=True)

        for file in os.listdir(args.folder):
            try:
                _, ext = file.rsplit(".", maxsplit=1)

                if ext in ("png", "jpg"):
                    path = os.path.join(args.folder, file)
                    img = frame_image(path, border=border, color=color)
                    img.save(os.path.join(output, file))
            except ValueError:
                pass

        return 0


#
# Parent
#


class Marketing(ParentCommand):
    """Utility to manipulate images for marketing purposes"""

    name: str = "marketing"

    @staticmethod
    def module():
        import uetools.plugins.gamekit.marketing

        return uetools.plugins.gamekit.marketing

    @staticmethod
    def fetch_commands():
        return [
            TemplateImg,
            ResizeImg,
            ShowcasheImg,
            FrameImg,
        ]


COMMANDS = Marketing
