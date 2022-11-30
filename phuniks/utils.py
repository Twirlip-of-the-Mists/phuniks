import random, colorsys

from kivy.app import App

#import pymunk

def pathto(filename):
    package = App.get_running_app().package
    return str(package/filename)

def random_colour():
    hue = random.uniform(0.0, 1.0)
    saturation = random.uniform(0.5, 1.0)
    value = random.uniform(0.5, 1.0)
    red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
    return int(red*255), int(green*255), int(blue*255)

def things_covering_position(space, position):
    things_found = []
    for thing in space.things:
        for shape in thing.shapes:
            point_query_info = shape.point_query(position)
            if point_query_info.distance < 0:
                things_found.append(thing)
                break
    return things_found
