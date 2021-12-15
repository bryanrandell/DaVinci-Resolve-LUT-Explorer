from PIL import Image
from itertools import chain
from PIL import ImageFilter
import tempfile
from base64 import b64decode


def load_cube_file(lines, target_mode=None, cls=ImageFilter.Color3DLUT):
    """Loads 3D lookup table from .cube file format.
    :param lines: Filename or iterable list of strings with file content.
    :param target_mode: Image mode which should be after color transformation.
                        The default is None, which means mode doesn't change.
    :param cls: A class which handles the parsed file.
                Default is ``ImageFilter.Color3DLUT``.
    """
    name, size = None, None
    channels = 3
    file = None

    lines = open(lines, 'rt')

    try:
        iterator = iter(lines)

        for i, line in enumerate(iterator, 1):
            line = line.strip()
            if line.startswith('TITLE "'):
                name = line.split('"')[1]
                continue
            if line.startswith('LUT_3D_SIZE '):
                size = [int(x) for x in line.split()[1:]]
                if len(size) == 1:
                    size = size[0]
                continue
            if line.startswith('CHANNELS '):
                channels = int(line.split()[1])
            if line.startswith('LUT_1D_SIZE '):
                raise ValueError("1D LUT cube files aren't supported")

            try:
                float(line.partition(' ')[0])
            except ValueError:
                pass
            else:
                # Data starts
                break

        if size is None:
            raise ValueError('No size found in the file')

        table = []
        for i, line in enumerate(chain([line], iterator), i):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                pixel = [float(x) for x in line.split()]
            except ValueError:
                raise ValueError("Not a number on line {}".format(i))
            if len(pixel) != channels:
                raise ValueError(
                    "Wrong number of colors on line {}".format(i))
            table.extend(pixel)
    finally:
        if file is not None:
            file.close()

    instance = cls(size, table, channels=channels,
                   target_mode=target_mode, _copy_table=False)
    if name is not None:
        instance.name = name
    return instance


def lut(img_thumbnail, lut_path):

    # lut_path = 'C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\LUT\\Arri\\Girlsroom_LUT_200831.cube'
    image_path = '/img/icon.png'
    img_thumb_base_decode = b64decode(img_thumbnail["data"])
    img = Image.frombytes(img_thumbnail['format'].split()[0], (img_thumbnail['width'], img_thumbnail['height']),img_thumb_base_decode)

    # im = Image.open(image_path)
    im_with_lut = img.filter(load_cube_file(lut_path))
    # im.show()
    # im_with_lut.show()
    # im_with_lut.
    # file_path = 'C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\Workflow Integration Plugins\\img\\{}.png'.format(name)
    tmp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    im_with_lut.save(tmp_file)
    print(tmp_file.name)
    # Image.open(tmp_file).show()
    return tmp_file.name
