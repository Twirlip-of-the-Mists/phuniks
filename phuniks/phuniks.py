#!/usr/bin/env python3

import math #, time
import sys

if sys.version_info < (3, 9):
        import importlib_resources
else:
        import importlib.resources as importlib_resources
        
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color

import pymunk
from pymunk import Vec2d

from .commanding import command, on_command
from .menu_widget import MenuWidget
from .space_widget import SpaceWidget

from .makers import BrushMaker, CircleMaker, RectangleMaker, PolygonMaker, PlaneMaker
from .modders import Kill, Explode
from .mouse import Mouse

from .things import Polygon

class Phuniks():
    def __init__(self, master_widget, space_widget, menu_widget):    
        self.master_widget = master_widget
        self.space_widget = space_widget
        self.menu_widget = menu_widget

        # -- Pymunk
        self.space = pymunk.Space(threaded=True)
        self.space.gravity = (0.0, -980.0)
        self.space.damping = 0.999
        self.space.iterations = 10
        self.space.threads = 8 # >2 probably has no effect
        self.space.things = []

        self.iterations = 10
        self.mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.action = None # Widget currently being built
        self.actor = BrushMaker # Builder to invoke on mousedown
        self.paused = False
        
        self.things_selected = []
        
        self.shapeargs = {
            'density':1,
            'elasticity':0.8,
            'friction':0.8
        }

        on_command('Pause', lambda cmnd: self.pause(True))
        on_command('Play', lambda cmnd: self.pause(False))
        on_command('Make', self.make)
        on_command('Modify', self.modify)

        command('Control', 'Play')
        command('Tool', 'Brush')
                 
    def pause(self, state):
        print('Phuniks.pause', state)
        self.paused = state
        
    def make(self, cmnd, subcmnd):
        print('Phuniks.make', subcmnd)
        if subcmnd == 'Brush':
            self.actor = BrushMaker
        elif subcmnd == 'Circle':
            self.actor = CircleMaker
        elif subcmnd == 'Rectangle':
            self.actor = RectangleMaker
        elif subcmnd == 'Polygon':
            self.actor = PolygonMaker
        elif subcmnd == 'Plane':
            self.actor = PlaneMaker

    def modify(self, cmnd, subcmnd):
        print('Phuniks.modify', subcmnd)
        if subcmnd == 'Kill':
            self.actor = Kill
        elif subcmnd == 'Explode':
            self.actor = Explode
        
    def mouse_kwargs(self, position, modifiers=None):
        position = Vec2d(*position)
        return {
            'position': position,
            'modifiers': modifiers,
            'mouse_body': self.mouse_body,
            'space': self.space,
            'space_widget': self.space_widget,
            'shapeargs': self.shapeargs
        }

    def step(self, dt):
        if not self.paused:
            for _ in range(self.iterations): # 10 iterations to get a more stable simulation
                self.space.step(dt / self.iterations)

class MasterWidget(FloatLayout):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #def build(self):
        #print('master build')
        space_widget = SpaceWidget(size=self.size)
        self.add_widget(space_widget)
        menu_widget = MenuWidget(size=self.size)
        self.add_widget(menu_widget)
        self.phuniks = Phuniks(self, space_widget, menu_widget)
        
    def on_touch_down(self, touch):
        #print('MasterWidget on_touch_down', touch.pos)
        phuniks = self.phuniks
        if phuniks.menu_widget.on_touch_down(touch):
            pass
        elif touch.button == 'scrolldown':
            command('ViewZoom', 'In', touch.pos)
        elif touch.button == 'scrollup':
            command('ViewZoom', 'Out', touch.pos)
        elif touch.button == 'left':
            position = Vector(phuniks.space_widget.to_local(*touch.pos))
            if not phuniks.action:
                phuniks.action = phuniks.actor()
                phuniks.action.mouse_click(**phuniks.mouse_kwargs(position, None))
            else:
                phuniks.action.mouse_click(**phuniks.mouse_kwargs(position, None))
        return True
        #else:
        #  return self.pf_space_widget.on_touch_down(touch)
    
    def on_touch_move(self, touch):
        phuniks = self.phuniks
        #print('on_touch_move', touch, touch.button)
        #print('pos', touch.pos)
        position = Vector(phuniks.space_widget.to_local(*touch.pos))
        if touch.button == 'left':
            if phuniks.action:
                phuniks.action.mouse_drag(**phuniks.mouse_kwargs(position, None))

    def on_touch_up(self, touch):
        phuniks = self.phuniks
        #print('on_touch_up', touch, touch.button)
        position = Vector(phuniks.space_widget.to_local(*touch.pos))
        if touch.button == 'left':
            if phuniks.action:
                result = phuniks.action.mouse_release(**phuniks.mouse_kwargs(position, None))
                if result != Mouse.ONGOING:
                    phuniks.action = None 
                if result == Mouse.ABANDONED:
                    pass# phuniks.undo_list.unpush()

    def my_mouse_pos(self, window_position):
        pass
 
    def update(self, dt):
        #print('Update')
        if self.phuniks.space.things and not self.phuniks.paused:
            thing = self.phuniks.space.things[0]
            #print('  ', thing.widget.__class__.__name__, thing.body.position)
            self.phuniks.step(dt)
            #print('  ', thing.widget.__class__.__name__, thing.body.position)
            #n=1
            for thing in self.phuniks.space.things:
                #if type(thing) != Anchor:
                #print('  Before', n, thing.widget.__class__.__name__, thing.body.position)
                thing.widget.position = thing.body.position
                thing.widget.angle = math.degrees(thing.body.angle)
                #print('  After', n, thing.widget.__class__.__name__, thing.body.position)
                #n+=1
            #if n > 2:
                #self.phuniks.paused = True
                #sys.exit(0)
                #thing.widget.angle = math.degrees(thing.body.angle)

class PhuniksApp(App):
    package = importlib_resources.files("phuniks")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_keyboard = Window.request_keyboard(self.my_keyboard_closed, self.root)
        self.my_keyboard.bind(on_key_down=self.my_on_keyboard_down)

    def my_keyboard_closed(self):
        self.my_keyboard.unbind(on_key_down=self.my_on_keyboard_down)
        self.my_keyboard = None

    def my_on_keyboard_down(self, keyboard, keycode, text, modifiers):
        m = set(modifiers)
        if m == set([]):
            if text == 'b':
                command('Tool', 'Brush')
            elif text == 'u':
                self.menu_widget.popup(Button(text='Hello'), pos=(self.width/2, self.height/2))
            elif text == 'z':
                command('ViewZoom', 'In')
                #self.menu_widget.set_option('Density', 1)
                #self.menu_widget.set_option('Friction', 1)
                #self.menu_widget.set_option('Elasticity', 1)
                #self.menu_widget.set_option('Shape color', [0,1,0,1])
            elif text == 'c':
                command('Tool', 'Circle')
            elif text == 'r':
                command('Tool', 'Rectangle')
            elif text == 'p':
                command('Tool', 'Polygon')
            elif text == 'n':
                command('Tool', 'Plane')
            elif text == 'a':
                command('Tool', 'Attach')
            elif text == 'h':
                command('Tool', 'Hinge')
            elif text == 's':
                command('Tool', 'Spring')
            elif text == 'g':
                command('Tool', 'Grab')
            elif text == 'm':
                command('Tool', 'Select')
            elif text == 'k':
                command('Tool', 'Kill')
            elif text == 'e':
                command('Tool', 'Explode')
            elif keycode[1] == 'spacebar':
                command('Control', 'Pause/Play')
            elif keycode[1] == 'end':
                command('Control', 'End')
            elif keycode[1] == 'home':
                command('Control', 'Start')
            elif keycode[1] == 'pagedown':
                command('Control', 'FastForward')
            elif keycode[1] == 'pageup':
                command('Control', 'Rewind')
            else:
                print(keyboard, keycode, text, modifiers)
        elif m == set(['ctrl']):
            if text == 'z':
                command('Control', 'Rewind')
            else:
                print(keyboard, keycode, text, modifiers)
        elif m == set(['ctrl', 'shift']):
            if text == 'z':
                command('Control', 'FastForward')
            else:
                print(keyboard, keycode, text, modifiers)
        elif m == set(['alt']):
            if text == 't':
                command('Main', 'Tools...')
            if text == 'c':
                command('Main', 'Controls...')
            if text == 'o':
                command('Main', 'Options...')
            if text == 's':
                command('Main', 'Shape...')
            else:
                print(keyboard, keycode, text, modifiers)
        else:
            print(keyboard, keycode, text, modifiers)
        return True
    
    def my_mouse_pos(self, one, position):
        #print('my_on_motion', one, position)
        self.master_widget.my_mouse_pos(position)
    
    def build(self):
        """Initializes the application; it will be called only once. If this method returns a widget (tree), it will be used as the root widget and added to the window."""
        
        print(Config.get('input', 'mouse'))
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
        #Config.set('graphics', 'multisamples', 4)
        
        Window.clearcolor = (1, 1, 1, 1)
        Window.set_title("Phuniks")
        width = 2560/2
        height = 1440/2
        Window.size = (width, height)
        Window.bind(mouse_pos=self.my_mouse_pos)

        self.master_widget = MasterWidget(size=Window.size)
        print(Window.size)
        
        Clock.schedule_interval(self.master_widget.update, 1.0/60.0)

        phuniks = self.master_widget.phuniks
        width = phuniks.space_widget.size[0]
        vertices = [
            Vec2d(0, 0),
            Vec2d(width-100, 0),
            Vec2d(width-100, 50),
            Vec2d(0, 50)
        ]
        #thing = Polygon(Vec2d(50,10), vertices, fixed=True)
        #thing.add_to_space(self.space, self.space_widget)

        #vertices = [Vec2d(0, 0), Vec2d(s.x, 0), Vec2d(s.x, s.y), Vec2d(0, s.y)]
        thing = Polygon(Vec2d(50,10), 0, Color(1,0,0), phuniks.shapeargs, vertices, fixed=True)
        print(vertices)
        thing.add_to_space(phuniks.space, phuniks.space_widget)

        return self.master_widget

def main():
    #if __name__ == '__main__':
    PhuniksApp().run()
