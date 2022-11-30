from kivy.uix.label import Label
#from kivy.app import App
#from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.properties import BoundedNumericProperty, ReferenceListProperty, OptionProperty, AliasProperty, StringProperty, BooleanProperty
from kivy.graphics.vertex_instructions import BorderImage
from kivy.uix.button import Button

# convert dvd-icons-35680_960_720.png -colorspace gray -colorspace RGB -contrast-stretch 0 dvd_greyscale.png
# convert dvd_greyscale.png -colorspace RGB -size 1x1 xc:'rgb(47, 167, 212)' -fx 'u*v.p{0,0}' dvd_coloured.png
# convert dvd_coloured.png -brightness-contrast 20x0 -contrast-stretch 0 dvd_brightened.png ; display dvd_brightened.png

from .utils import pathto

class PopupMenu(DragBehavior, RelativeLayout):
    
    def get_content_width(self):
        return self.width - 2 * self.border
    
    def set_content_width(self, width):
        self.width = width + 2 * self.border

    def get_content_height(self):
        #try:
        value = self.height - 2*self.border - self.title_label.height - 2*self.spacing - self.separator
        #except AttributeError: # self.title might not exist yet
        #  value = self.height - 2 * self.border_thickness - 2 * self.padding_thickness
        return value
    
    def set_content_height(self, height):
        old_height = self.height
        new_height = height + 2*self.border + self.title_label.height + 2*self.spacing + self.separator
        new_y = self.y - (new_height - self.height)
        (self.y, self.height) = (new_y, new_height) 

    border = BoundedNumericProperty(5, min=0)
    spacing = BoundedNumericProperty(5, min=0)
    separator = BoundedNumericProperty(2, min=0)
    title = StringProperty('Title')
    vertical = BooleanProperty(True)

    background_r = BoundedNumericProperty(0.18, min=0.0, max=1.0)
    background_g = BoundedNumericProperty(0.18, min=0.0, max=1.0)
    background_b = BoundedNumericProperty(0.18, min=0.0, max=1.0)
    background_a = BoundedNumericProperty(0.5, min=0.0, max=1.0)
    background_color = ReferenceListProperty(background_r, background_g, background_b, background_a)

    separator_r = BoundedNumericProperty(47/255, min=0.0, max=1.0)
    separator_g = BoundedNumericProperty(167/255, min=0.0, max=1.0)
    separator_b = BoundedNumericProperty(212/255, min=0.0, max=1.0)
    separator_a = BoundedNumericProperty(1.0, min=0.0, max=1.0)
    separator_color = ReferenceListProperty(separator_r, separator_g, separator_b, separator_a)

    content_width = AliasProperty(get_content_width, set_content_width, bind=['width', 'border'])
    content_height = AliasProperty(get_content_height, set_content_height, bind=['height', 'border', 'separator'])
    content_size = ReferenceListProperty(content_width, content_height)

    parent_hsize_hint = OptionProperty('nearest', options=['left', 'right', 'nearest'])
    parent_vsize_hint = OptionProperty('nearest', options=['top', 'bottom', 'nearest'])
    parent_resize_hint = ReferenceListProperty(parent_hsize_hint, parent_vsize_hint)
    
    def __init__(self, title, border=5, spacing=5, separator=2, separator_color=(47/255, 167/255, 212/255, 1), background_color=(0.0, 0.0, 0.0, 0.65), closable=True, parent_resize_hint=('nearest', 'nearest'), vertical=True, *args, **kwargs):
        super().__init__(*args, size_hint=(None,None), **kwargs)
        
        self.title = title
        self.border = border
        self.spacing = spacing
        self.separator_color = separator_color
        self.background_color = background_color
        self.separator = separator
        self.parent_resize_hint = parent_resize_hint
        self.vertical = vertical
        
        self.drag_timeout = 10000000
        self.drag_distance = 0

        with self.canvas:
            self.border_image = BorderImage(size=(self.width + 10, self.height + 10), pos=(-8, -12), source=pathto('images/shadow.png'), border=(10,10,40,40))
            self.background_rectangle_color = Color(*self.background_color)
            self.background_rectangle = RoundedRectangle(pos=(0, 0), size=self.size, radius=(2,2))

            self.separator_rectangle_color = Color(*self.separator_color)
            self.separator_rectangle = Rectangle(pos=(0, 0), size=self.size)

        self.title_label = Label(text=self.title, size_hint=(None, None))
        self.title_label.texture_update()
        self.title_label.size = self.title_label.texture_size
        self.add_widget(self.title_label)
        
        if closable:
            self.close_button = Button(text=' X ', size_hint=(None, None), on_release=self._on_close)
            self.close_button.texture_update()
            self.close_button.size = self.close_button.texture_size
            self.add_widget(self.close_button)
        else:
            self.close_button = None

        self.content_height = 0
        self.resize()
        self.recolor()
        self.bind(border=self.resize)
        self.bind(border=self.resize)
        self.bind(spacing=self.on_children)
        self.bind(background_color=self.recolor)
        self.bind(separator_color=self.recolor)

    def on_size(self, *args, **kwargs):
        self.resize()

    def _on_close(self, *args, **kwargs):
        self.on_close(self, self)

    def on_close(self, instance, value):
        #print('on_close')
        pass
        
    def recolor(self):
        self.background_rectangle_color.rgba = self.background_color
        self.separator_rectangle_color.rgba = self.separator_color
        
    def resize(self):
        self.title_label.width = self.width - 2*self.border
        self.title_label.x = self.border
        self.title_label.y = self.height - self.border - self.title_label.height

        if self.close_button:
            self.close_button.x = self.width - self.close_button.width - self.border
            self.close_button.y = self.height - self.close_button.height - self.border
            self.title_label.width -= self.close_button.width

        self.title_label.text_size[0] = self.title_label.width
        
        self.background_rectangle.size = self.size
        self.border_image.size = (self.width + 12, self.height + 12)
        self.border_image.pos = (-5, -7)

        self.separator_rectangle.size = (self.width - 2*self.border, self.separator)
        self.separator_rectangle.pos = (self.border, self.height - self.border - self.title_label.height - self.spacing - self.separator)
        self.calc_distances_to_parent()
        self.calc_drag_rectangle()

    def calc_drag_rectangle(self):
        try:
            pos = (self.x, self.y + self.height - self.border - self.title_label.height - self.spacing)
            size = (self.border + self.title_label.width, self.border + self.title_label.height + self.spacing)
            self.drag_rectangle = [*pos, *size]
        except AttributeError: # Can get called before self.title_label exists
            pass
        
    def on_pos(self, *args, **kwargs):
        self.calc_drag_rectangle()
        self.calc_distances_to_parent()
        
    def on_children(self, *args, **kwargs):
        if self.vertical:
            self.on_children_vertical(*args, **kwargs)
        else:
            self.on_children_horizontal(*args, **kwargs)
            
    def on_children_horizontal(self, *args, **kwargs):
        # Must have at least title and close_button for this to work
        if len(self.children) < 2: return
        content_height = 0
        content_width = 0
        for child in reversed(self.children):
            if child is not self.title_label and child is not self.close_button:
                child.size_hint = (None, None)
                child.x = self.border + content_width
                child.y = self.border
                content_width += child.width + self.spacing
                if child.height > content_height:
                    content_height = child.height
        self.content_height = content_height
        self.content_width = content_width - self.spacing
        self.resize()
    
    def on_children_vertical(self, *args, **kwargs):
        # Must have at least title and close_button for this to work
        if len(self.children) < 2: return
        content_height = 0
        content_width = self.title_label.width
        if self.close_button:
            content_width += self.close_button.width
        for child in self.children:
            if child is not self.title_label and child is not self.close_button:
                child.size_hint = (None, None)
                child.x = self.border
                child.y = self.border + content_height
                content_height += child.height + self.spacing
                if child.width > content_width:
                    content_width = child.width
        self.content_height = content_height - self.spacing
        self.content_width = content_width
        self.resize()

    def on_parent(self, *args, **kwargs):
        if self.parent is not None:
            self.calc_distances_to_parent()
            self.move_inside_parent()
            self.parent.bind(size=self.on_parent_size)
        
    def on_parent_size(self, *args, **kwargs):
        if self.parent is not None:
            x = self.x
            y = self.y
            if (  (self.parent_hsize_hint == 'nearest' and self.to_right < self.to_left) or
                        (self.parent_hsize_hint == 'right')  ):
                    x = self.parent.x + self.parent.width - self.to_right - self.width
            if (  (self.parent_vsize_hint == 'nearest' and self.to_top < self.to_bottom) or
                        (self.parent_vsize_hint == 'top')  ):
                    y = self.parent.y + self.parent.height - self.to_top - self.height
            self.pos = (x, y) # Will trigger on_pos

    def calc_distances_to_parent(self): 
        if self.parent:
            self.to_left = self.x - self.parent.x
            self.to_right = self.parent.x + self.parent.width - self.x - self.width
            self.to_bottom = self.y - self.parent.y
            self.to_top = self.parent.y + self.parent.height - self.y - self.height

    def move_inside_parent(self):
        # FIXME This could recurse for ever
        if self.parent:
            if (self.to_left < 0) and not (self.to_right < 0):
                self.x -= self.to_left
            elif (self.to_right < 0) and not (self.to_left < 0):
                self.x += self.to_right
                
            if (self.to_bottom < 0) and not (self.to_top < 0):
                self.y -= self.to_bottom
            elif (self.to_top < 0) and not (self.to_bottom < 0):
                self.y += self.to_top

    def my_on_keyboard_down(self, keyboard, keycode, text, modifiers):
        pass

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            parent = self.parent
            parent.remove_widget(self)
            parent.add_widget(self)
            super().on_touch_down(touch)
            return True
        return False
