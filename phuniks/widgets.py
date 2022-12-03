from random import random

from kivy.uix.widget import Widget
from kivy.graphics.tesselator import Tesselator
from kivy.vector import Vector
from kivy.graphics import PushMatrix, PopMatrix, Translate, Rotate, Scale, Rectangle, Color, Line, Ellipse, Mesh

from .utils import pairwise    

class MarkerWidget(Widget):
    marker_colour = (1, 0, 0)
    marker_radius = 5
  
class DotWidget(MarkerWidget):
    def __init__(self, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rad = self.marker_radius
        with self.canvas:
            Color(self.marker_colour)
            Ellipse(pos=(position[0]-rad, position[1]-rad), size=(2*rad, 2*rad))
  
class MovableWidget(Widget):
    border_width = 2
    
    def __init__(self, position=(0,0), angle=0, offset=(0,0), *args, **kwargs):
        super().__init__(*args, **kwargs)
        with self.canvas.before:
            PushMatrix()
            self.body_translate = Translate(*position)
            self.body_rotate = Rotate(angle, origin=(0,0))
            self.offset_translate = Translate(*offset)
        with self.canvas:
            self.color = Color(random(), random(), random())
        with self.canvas.after:
            PopMatrix()
  
    @property
    def position(self):
        return Vector(self.body_translate.x, self.body_translate.y)

    @position.setter
    def position(self, value):
        self.body_translate.x = value[0]
        self.body_translate.y = value[1]
  
    @property
    def angle(self):
        return self.body_rotate.angle

    @angle.setter
    def angle(self, value):
        self.body_rotate.angle = value
  
    @property
    def offset(self):
        return Vector(self.offset_translate.x, self.offset_translate.y)

    @offset.setter
    def offset(self, value):
        self.offset_translate.x = value[0]
        self.offset_translate.y = value[1]
  
    #def unwidget(self):
        #self.parent.remove_widget(self)
  
class OutlineWidget(MovableWidget):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        with self.canvas:
            Color(0, 0, 0)
            self.line = Line(points=[0,0], width=self.border_width)
            #self.tentative = Line(points=[0,0,0,0], width=1)
    
    def append(self, point):
        self.line.points.append(point[0])
        self.line.points.append(point[1])
        self.line.points = self.line.points
      
    def points(self):
        return list(pairwise(self.line.points))
    
    #def update(self, point):
    #    self.border.points[-2] = point[0]
    #    self.border.points[-1] = point[1]
    #    self.border.points = self.border.points
      
    #def guess(self, point):
    #    self.tentative.points[-4] = self.border.points[-2]
    #    self.tentative.points[-3] = self.border.points[-1]
    #    self.tentative.points[-2] = point[0]
    #    self.tentative.points[-1] = point[1]
    #    self.tentative.points = self.tentative.points
      
class PolygonWidget(MovableWidget):
    def __init__(self, vertices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        points = []
        for vertex in vertices:
            points.append(vertex[0])
            points.append(vertex[1])
        #print(points)
        tesselator = Tesselator()
        tesselator.add_contour(points)
        tesselator.tesselate()
        with self.canvas:
            for vertices, indices in tesselator.meshes:
                Mesh(vertices=vertices, indices=indices, mode="triangle_fan")
            Color(0, 0, 0)
            self.border = Line(points=points, width=self.border_width, close=True)

class RectangleWidget(MovableWidget):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        with self.canvas:
            self.rectangle = Rectangle(pos=(0,0), size=(0,0))
            Color(0, 0, 0)
            self.border = Line(rectangle=(0, 0, 0, 0), width=self.border_width)

    @property
    def size(self):
        return self.rectangle.size
  
    @size.setter
    def size(self, value):
        new_size = Vector(value)
        self.rectangle.size = new_size
        self.canvas.remove(self.border)
        with self.canvas:
            self.border = Line(rectangle=(0, 0, new_size.x, new_size.y), width=self.border_width)

class CircleWidget(MovableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with self.canvas:
            self.ellipse = Ellipse(pos=(-1, -1), size=(2, 2))
            Color(0, 0, 0)
            self.spoke = Line(points=[(0, 0), (0, 1)], width=2)
            self.border = Line(circle=(0, 0, 1), width=3)

    @property
    def radius(self):
        return self.ellipse.size / 2
  
    @radius.setter
    def radius(self, value):
        new_radius = float(value)
        # FIXME assumes centre is at (0, 0). Should calculate from old radius & position
        self.ellipse.pos = Vector(-new_radius, -new_radius)
        self.ellipse.size = Vector(new_radius*2, new_radius*2)
        self.canvas.remove(self.spoke)
        self.canvas.remove(self.border)
        with self.canvas:
            self.spoke = Line(points=[(0, 0), (0, new_radius)], width=self.border_width/2)
            self.border = Line(circle=(0, 0, new_radius), width=self.border_width)

class DropletWidget(MovableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color.rgba = Color(0, 0, 0.7).rgba
        with self.canvas:
            self.ellipse = Ellipse(pos=(-1, -1), size=(2, 2))

    @property
    def radius(self):
        return self.ellipse.size / 2
  
    @radius.setter
    def radius(self, value):
        new_radius = float(value)
        # FIXME assumes centre is at (0, 0). Should calculate from old radius & position
        self.ellipse.pos = Vector(-new_radius, -new_radius)
        self.ellipse.size = Vector(new_radius*2, new_radius*2)
