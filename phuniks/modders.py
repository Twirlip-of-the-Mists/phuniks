import pymunk
from pymunk import Vec2d

from .mouse import Mouse
from .utils import things_covering_position
from .things import Droplet

#================================ Killer ================================+

def kill(thing, space, space_widget, things_selected=[]):
    if thing.selected:
        things = things_selected.copy()
        things_selected[:] = []
    else:
        things = [thing]
    for thing in things:
        #thing.widget.unwidget()
        thing.remove_from_space(space, space_widget)
        
class Kill(Mouse):
    def mouse_click(self, position, space, space_widget, **kwargs):
        things_clicked = things_covering_position(space, position)
        things_selected = [] #things_currently_selected(space)
        if things_clicked:
            kill(things_clicked[-1], space, space_widget, things_selected)
            self.result = self.COMPLETE

#================================ Explode ================================+

def overlay_with_circles(space, space_widget, body, radius=10):
    for shape in body.shapes:
        spacing = int(radius)
        shape.cache_bb()
        #print('Bounding box', shape.bb)
        y_spacing = int(2 * spacing * 0.86602540378) # cosine(30)
        for x in range(int(shape.bb.left), int(shape.bb.right), 2*int(spacing)):
            for y in range(int(shape.bb.bottom), int(shape.bb.top), 2*y_spacing):
                point_query_info = shape.point_query((x,y))
                if point_query_info.distance < -radius:
                    thing = Droplet(Vec2d(x,y), radius)
                    thing.add_to_space(space, space_widget)
                    #FunCircle.make(Vec2d(x,y), radius, dispinfo, space=space, friction=friction, colour=colour, border=False)
        for x in range(int(shape.bb.left)+int(spacing), int(shape.bb.right), 2*int(spacing)):
            for y in range(int(shape.bb.bottom)+y_spacing, int(shape.bb.top), 2*y_spacing):
                point_query_info = shape.point_query((x,y))
                if point_query_info.distance < -radius:
                    thing = Droplet(Vec2d(x,y), radius)
                    thing.add_to_space(space, space_widget)

def explode(thing, space, space_widget, things_selected=[]):
    if thing.selected:
        things = things_selected.copy()
        things_selected[:] = []
    else:
        things = [thing]
    for thing in things:
        overlay_with_circles(space, space_widget, thing)
        #thing.widget.unwidget()
        thing.remove_from_space(space, space_widget)
        
class Explode(Mouse):
    def mouse_click(self, position, space, space_widget, **kwargs):
        things_clicked = things_covering_position(space, position)
        things_selected = [] #things_currently_selected(space)
        if things_clicked:
            explode(things_clicked[-1], space, space_widget, things_selected)
            self.result = self.COMPLETE
