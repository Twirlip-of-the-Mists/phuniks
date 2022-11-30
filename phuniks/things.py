import pymunk
from pymunk import Vec2d
import pymunk.autogeometry

from .widgets import CircleWidget, DropletWidget, PolygonWidget

def body_make(position, angle, fixed=False):
    if fixed:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
    else:
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = position
    body.velocity = Vec2d(0.0, 0.0)
    body.angular_velocity = 0.0
    body.angle = angle
    return body

class Thing():
    """Base class for all things"""

    next_tid = 0
  
    def __init__(self):
        #self.tid = Thing.next_tid
        #Thing.next_tid += 1
        self.selected = False
        #self.marked = False
        #self.joins_as_a = []
        #self.joins_as_b = []

        # Kivy
        self.widget = None

        #PyMunk
        self.body = None
        self.shapes = []

    def __getstate__(self):
        state = self.__dict__.copy()
        state['widget'] = None
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.create_widget()

    def add_to_space(self, space, space_widget):
        space.add(self.body, *self.shapes)
        #print(self.body.position)
        #space.step(1)
        #print(self.body.position)
        space.things.append(self)
        space_widget.add_widget(self.widget)
    
    def remove_from_space(self, space, space_widget):
        space.remove(self.body, *self.shapes)
        space.things.remove(self)
        print(space_widget)
        space_widget.remove_widget(self.widget)

    def apply_shape_args(self, shapeargs):
        for shape in self.shapes:
            for key, value in shapeargs.items():
                #print('setattr(', shape, key, value, ')')
                setattr(shape, key, value)
        
#============================== Circle ==============================

class Circle(Thing):
    """A circle. Has a single pymunk circle as its only shape"""
   
    def __init__(self, position, angle, color, shapeargs, radius, offset=(0,0)):
        super().__init__()
        self.color = color
        self.body = body_make(position, angle)
        self.body.things = [self]
        shape = pymunk.Circle(self.body, radius, offset)
        shape.thing = self
        self.shapes.append(shape)
        self.apply_shape_args(shapeargs)
        self.create_widget()
    
    def create_widget(self):
        self.widget = CircleWidget()
        self.widget.position = self.body.position
        self.widget.angle = self.body.angle
        self.widget.color.rgba = self.color.rgba
        self.widget.radius = self.shapes[0].radius
        self.widget.offset = self.shapes[0].offset
    
#============================== Droplet ==============================

class Droplet(Thing):
    """A water droplet. Has a single pymunk circle as its only shape"""
   
    def __init__(self, position, radius):
        super().__init__()
 
        shapeargs = {
            'density':1,
            'elasticity':0,
            'friction':0
        }

        self.body = body_make(position, 0)
        self.body.things = [self]
        shape = pymunk.Circle(self.body, radius)
        shape.thing = self
        self.shapes.append(shape)
        self.apply_shape_args(shapeargs)
        self.create_widget()
    
    def create_widget(self):
        self.widget = DropletWidget()
        self.widget.position = self.body.position
        self.widget.angle = self.body.angle
        self.widget.radius = self.shapes[0].radius
        self.widget.offset = self.shapes[0].offset

#============================== Polygon ==============================

class Polygon(Thing):
    """A possibly concave polygon. Has one of more pymunk convex polys as its shapes"""

    def __init__(self, position, angle, color, shapeargs, vertices, fixed=False, tolerance=1.0):
        super().__init__()
        self.color = color
        self.body = body_make(position, angle, fixed=fixed)
        self.body.things = [self]

        self.vertices = pymunk.autogeometry.simplify_curves(vertices, tolerance)
        # PyMunk's convex_decomposition expects a closed polygons
        if not pymunk.autogeometry.is_closed(self.vertices):
            self.vertices.append(vertices[0])
        convex_polygons = pymunk.autogeometry.convex_decomposition(self.vertices, tolerance)
    
        for convex_polygon in convex_polygons:
            shape = pymunk.Poly(self.body, convex_polygon)
            #set_shape_attrs(shape, **kwargs)
            shape.thing = self
            self.shapes.append(shape)
        self.apply_shape_args(shapeargs)
        self.create_widget()
    
    def create_widget(self):
        self.widget = PolygonWidget(self.vertices)
        self.widget.position = self.body.position
        self.widget.angle = self.body.angle
        self.widget.color.rgba = self.color.rgba


