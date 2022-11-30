from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.image import Image

class LabeledCheckBox(RelativeLayout):
    def __init__(self, text, on_value=None, *args, **kwargs):
        super().__init__()
        
        self.label = Button(text=text, size_hint=(None,None), background_color=(0,0,0,0), on_press=self.toggle)
        self.label.texture_update()
        self.label.size = (self.label.texture_size[0] + 10,  self.label.texture_size[1] + 10)
        self.label.pos = (self.label.height, 0)

        self.checkbox = CheckBox(size_hint=(None,None), *args, **kwargs) 
        self.checkbox.pos = (0, 0)
        self.checkbox.size = (self.label.height, self.label.height)
        
        self.size = (self.label.width + self.label.height, self.label.height)

        self.add_widget(self.label)
        self.add_widget(self.checkbox)
    
    def toggle(self, instance):
        self.checkbox.active = not self.checkbox.active
    
    def trigger_action(self, duration=0.1):
        self.toggle(self)
            
class LabeledSlider(RelativeLayout):
    text = StringProperty('Value')

    def __init__(self, text='Value', to_string=None, *args, **kwargs):
        super().__init__()

        self.text = text
        if to_string:
            self.to_string = to_string

        self.slider = Slider(size_hint=(None, None), *args, **kwargs)
        
        valuestr = self.to_string(self, self.slider, self.text, self.slider.value)
        self.label = Label(text=valuestr, size_hint=(None, None),)
        self.label.texture_update()
        self.label.size = (self.slider.width,  self.label.texture_size[1])
        self.label.text_size = self.label.size
        
        self.size = (self.slider.width, self.slider.height + self.label.height)
        self.label.pos = ((self.width - self.label.width)/2, self.slider.height)
        self.slider.pos = ((self.width - self.slider.width)/2, 0)
        self.slider.bind(value=self.update_label)
        
        self.add_widget(self.label)
        self.add_widget(self.slider)
        
    def update_label(self, instance, value):
        self.label.text = self.to_string(self, self.slider, self.text, value)
        
    def call_to_string(self, instance1, instance2, value):
        return self.to_string(self, self.slider, self.text, value)
    
    def to_string(self, instance, slider, text, value):
        if type(value) is float:
            return f'{text} = {value:.{4}}'
        else:
            return f'{text} = {value}'
    
class ImageButton(Button):
    def __init__(self, source, margin=5, *args, **kwargs):
        super().__init__(size_hint=(None, None), *args, **kwargs)
        self.margin = margin
        self.image = Image(source=source)
        self.image.texture_update()
        self.image.size = self.image.texture_size
        self.image.pos = (self.x+self.margin, self.y+self.margin)
        self.add_widget(self.image)
        self.size = (self.image.width+2*self.margin, self.image.height+2*self.margin)

    def on_pos(self, instance, value):
        self.image.pos = (self.x+self.margin, self.y+self.margin)
        
class ImageToggleButton(ToggleButton):
    def __init__(self, source, margin=5, *args, **kwargs):
        super().__init__(size_hint=(None, None), *args, **kwargs)
        self.margin = margin
        self.image = Image(source=source)
        self.image.texture_update()
        self.image.size = self.image.texture_size
        self.image.pos = (self.x+self.margin, self.y+self.margin)
        self.add_widget(self.image)
        self.size = (self.image.width+2*self.margin, self.image.height+2*self.margin)
        
    def on_pos(self, instance, value):
        self.image.pos = (self.x+self.margin, self.y+self.margin)
