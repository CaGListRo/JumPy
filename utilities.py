import pygame as pg

def load_image(imagename):
    img = pg.image.load('images/' + imagename + '.png').convert_alpha()
    return img