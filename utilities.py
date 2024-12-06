import pygame as pg

def load_image(imagename: str) -> pg.Surface:
    """
    Load an image from a file.
    Args:
    imagename (str): The name of the image. (Without ".png")
    Returns:
    pg.Surface: The loaded image.
    """
    img: pg.Surface = pg.image.load('images/' + imagename + '.png').convert_alpha()
    return img