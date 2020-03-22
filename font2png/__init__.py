import os
from typing import Dict
from typing import Union

import fontforge

Font2PNGError = type("Font2PNGError", (BaseException,), {})
FileTypeNotSupported = type("FileTypeNotSupported", (Font2PNGError,), {})


def font2png(font_file: str,
             png_dir: Union[None, str] = None,
             png_height: int = 500) -> Dict[str, dict]:
    """
    convert every character in font_file  to png picture, holded by png_dir
    :param font_file: the font file, supports ttf and woff2
    :param png_dir: the directory holding the exported png files
    :param png_height: the height of every png picture, the wide is auto adjusted
    :return: a dict holds the mapping from character to it's picture
    """

    _SUPPORTED_FILE_TYPES = [".ttf", ".woff2"]

    # do the argument checking jobs, kinda messy
    assert os.path.exists(font_file)
    base, ext = os.path.splitext(font_file)
    if not ext in _SUPPORTED_FILE_TYPES:
        raise FileTypeNotSupported(f"file type [{ext}] is not in supporting list: {_SUPPORTED_FILE_TYPES}")

    if png_dir is None:
        png_dir = base
        if os.path.exists(png_dir) and os.path.isfile(png_dir):
            raise FileExistsError(f"png_dir is using default path [{png_dir}], but it's a file path")
        os.makedirs(png_dir, exist_ok=True)
    assert os.path.exists(png_dir)

    # the return value
    character_pictures: Dict[str, dict] = {}

    # start converting
    font_file_obj = fontforge.open(font_file)
    for character_name in font_file_obj:
        font = font_file_obj[character_name]
        code_point_base10 = font.encoding
        character = chr(code_point_base10)
        png_file = f"{png_dir}/{code_point_base10}.png"  # use code point as picture name, it's safe for naming a file
        os.makedirs(os.path.dirname(png_file), exist_ok=True)
        font.export(png_file, png_height)  # the exporting job is simple
        character_pictures[character] = {"png_path": png_file}
        print(f"{character} --> [w:x, h:{png_height}]{png_file}")

    return character_pictures
