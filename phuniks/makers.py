import pymunk
from pymunk import Vec2d

from .mouse import Mouse
from .widgets import CircleWidget, RectangleWidget, PolygonWidget
from .things import Circle, Polygon

class CircleMaker(Mouse):
    def mouse_click(self, position, space_widget, **kwarg):
        super().__init__()
        self.position = position
        self.radius = 4
        self.widget = CircleWidget(position=position)
        space_widget.add_widget(self.widget)
        
    def mouse_drag(self, position, **kwargs):
        self.radius = max(self.position.get_distance(position), 3)
        self.widget.radius = self.radius
        
    def mouse_release(self, space, space_widget, shapeargs, **kwargs):
        color = self.widget.color
        space_widget.remove_widget(self.widget)
        thing = Circle(self.position, 0, color, shapeargs, self.radius)
        thing.add_to_space(space, space_widget)
        return self.COMPLETE

class RectangleMaker(Mouse):
    def mouse_click(self, position, space_widget, **kwargs):
        self.position = position
        self.size = Vec2d(2,2)
        self.widget = RectangleWidget(position=position)
        space_widget.add_widget(self.widget)
        
    def mouse_drag(self, position, **kwargs):
        self.size = position - self.position
        self.widget.size = self.size

    def mouse_release(self, space, space_widget, shapeargs, **kwargs):
        s = self.size
        color = self.widget.color
        space_widget.remove_widget(self.widget)
        if (s.x > 0) == (s.y > 0):
            vertices = [Vec2d(0, 0), Vec2d(s.x, 0), Vec2d(s.x, s.y), Vec2d(0, s.y)]
        else:
            vertices = [Vec2d(0, 0), Vec2d(0, s.y), Vec2d(s.x, s.y), Vec2d(s.x, 0)]
        thing = Polygon(self.position, 0, color, shapeargs, vertices)
        thing.add_to_space(space, space_widget)
        return self.COMPLETE

class PlaneMaker(Mouse):
    def mouse_click(self, position, space_widget, **kwargs):
        infinity = 32786
        self.position = position
        self.vertices = [
            Vec2d(0, 0),
            Vec2d(infinity, 0),
            Vec2d(infinity, -infinity),
            Vec2d(-infinity, -infinity),
            Vec2d(-infinity, 0)
        ]
        self.widget = PolygonWidget(self.vertices, position=position)
        space_widget.add_widget(self.widget)
        
    def mouse_drag(self, position, **kwargs):
        print(self.position)
        print(position)
        self.widget.angle = (self.position - position).angle_degrees + 90

    def mouse_release(self, space, space_widget, shapeargs, **kwargs):
        color = self.widget.color
        angle = self.widget.angle
        space_widget.remove_widget(self.widget)
        thing = Polygon(self.position, angle, color, shapeargs, self.vertices, fixed=True)
        thing.add_to_space(space, space_widget)
        return self.COMPLETE

