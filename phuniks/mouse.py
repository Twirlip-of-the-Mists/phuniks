#import arcade

from .utils import random_colour

class Mouse():
    """Superclass for classes that respond to mouse events"""

    COMPLETE = 1
    ONGOING = 2
    ABANDONED = 3
    
    def __init__(self, colour=None):
        self.result = self.ABANDONED
         
    def mouse_click(self, **kwargs):
        pass
    
    def mouse_drag(self, **kwargs):
        pass
    
    def mouse_move(self, **kwargs):
        pass
    
    def mouse_release(self, **kwargs):
        return self.result
    
