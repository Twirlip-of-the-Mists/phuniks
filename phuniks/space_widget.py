from kivy.uix.scatter import Scatter
from kivy.vector import Vector
from kivy.graphics.transformation import Matrix

from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color

from .commanding import command, on_command

class SpaceWidget(Scatter):
    def __init__(self, *args, **kwargs):
        super().__init__(do_rotation=False, do_translation=False, do_scale=False, *args, **kwargs)
        on_command('Zoom', self.zoom)
    
    def zoom(self, cmnd, scale, pos):
        if pos:
            before = Vector(self.to_local(*pos))
        self.scale = scale
        if pos:
            after = Vector(self.to_local(*pos))
            diff = after - before
            self.apply_transform(Matrix().translate(diff.x, diff.y, 0), post_multiply=True)

    #def on_touch_down(self, touch):
        #if touch.button == 'scrolldown':
            #command('ViewZoom', 'In', touch.pos)
        #elif touch.button == 'scrollup':
            #command('ViewZoom', 'Out', touch.pos)
        ## We would use this to let 
        ## position = Vector(self.to_local(*pos))
        #return True
  
    #def on_touch_down_old(self, touch):
        #rescale = 1.05
        ##print('SpaceWidget on_touch_down', touch.pos)
        #position = Vector(self.to_local(*touch.pos))
        #if touch.button == 'scrolldown':
            #self.scale *= rescale
            #after = Vector(self.to_local(*touch.pos))
            #diff = after - position
            #self.apply_transform(Matrix().translate(diff.x, diff.y, 0), post_multiply=True)
            #retval = False
        #elif touch.button == 'scrollup':
            #self.scale /= rescale
            #after = Vector(self.to_local(*touch.pos))
            #diff = after - position
            #self.apply_transform(Matrix().translate(diff.x, diff.y, 0), post_multiply=True)
            #retval = False
        #else:
            #print('Pre transform', touch.pos, self.to_local(*touch.pos))
            #touch.push()
            #touch.apply_transform_2d(self.to_local)
            #print('Post transform', touch.pos)
            #retval = super().on_touch_down(touch)
            #touch.pop()
        #return retval
