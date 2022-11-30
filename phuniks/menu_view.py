import math

from .popup_menu_widgets import LabeledSlider
from .popup_menu import PopupMenu
from .commanding import command, on_command

class ViewMenu(PopupMenu):
    
    def __init__(self, on_close):  # Tools popup menu
        super().__init__('View', pos=(200,196))
        self.on_close = on_close
        self.zoom_about = None
        
        self.labeled_slider = LabeledSlider(text='Zoom', size=(200,30), min=-5, max=5, step=0.1, value=0, to_string=self.zoom_string)
        self.add_widget(self.labeled_slider)
        
        on_command('ViewZoom', self.zoom_command)
        
    #def on_active(self, instance, state):
    #  self.on_set_option(instance.label.text, state=='down')

    #def zoom_string(self, popup, spinner, text, value):
        #self.on_set_option('Zoom', math.pow(2, value))
        #return f'{text} = {math.pow(2, value)*100:.{5}}%'

    def zoom_string(self, popup, spinner, text, value):
        if not self.zoom_about and self.parent:
            self.zoom_about = (self.parent.width/2, self.parent.height/2)
        command('Zoom', math.pow(2, value), self.zoom_about)
        self.zoom_about = None
        return f'{text} = {math.pow(2, value)*100:.{5}}%'

    def zoom_command(self, cmnd, subcmnd, zoom_about=None):
        slider = self.labeled_slider.slider
        value = slider.value
        if subcmnd == 'In':
            value += slider.step
        else:
            value -= slider.step
        self.zoom_about = zoom_about
        slider.value = sorted((slider.min, value, slider.max))[1]
        
