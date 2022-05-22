from PIL import Image, ExifTags

from .config import Config


def transform_image(image: Image.Image, conf: Config) -> Image.Image:
    """
    Abstracted method to return desired image transformation.
    """
    image = _orient(image)
    return _pixalize(image, conf.image.pixel_count)


def _orient(image: Image.Image) -> Image.Image:
    """
    Fixes image orientation due to missing EXIF data.
    https://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
    """
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())
    rotation = {3: 180, 6: 270, 8: 90}.get(exif[orientation], 0)
    return image.rotate(rotation, expand=True)


def _pixalize(image: Image.Image, pixels: int) -> Image.Image:
    """
    Pixalize image by resizing smoothly down and scale back up.
    """
    imgSmall = image.resize((pixels, pixels), resample=Image.BILINEAR)
    return imgSmall.resize(image.size, Image.NEAREST)
