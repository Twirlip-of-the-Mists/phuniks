from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.properties import BoundedNumericProperty, ReferenceListProperty
from kivy.uix.popup import Popup

from .popup_menu_widgets import LabeledSlider
from .popup_menu import PopupMenu
from .commanding import command, on_command

class ColorPickerPopup(Popup):
    def __init__(self, color, on_color_save):  # Tools popup menu
        super().__init__(title='Choose colour', size_hint=(None, None), size=(600, 400))
        
        self.on_color_save = on_color_save
        buttonbar = StackLayout(orientation='rl-bt', size_hint=(1, None))
        content = BoxLayout(padding=10, orientation='vertical')
        
        cancel = Button(text='Cancel', size_hint=(None, None), on_press=self.cancel)
        cancel.texture_update()
        cancel.size = (cancel.texture_size[0] + 10, cancel.texture_size[1] + 10)
        buttonbar.height = cancel.height
        
        save = Button(text='Save', size_hint=(None, None), on_press=self.save)
        save.size = cancel.size

        self.color_picker = ColorPicker(color=color)
        
        buttonbar.add_widget(save)
        buttonbar.add_widget(cancel)
        content.add_widget(self.color_picker)
        content.add_widget(buttonbar)
        self.add_widget(content)

    def cancel(self, instance):
        self.dismiss()

    def save(self, instance):
        self.on_color_save(self.color_picker.color)
        self.dismiss()

class ShapeMenu(PopupMenu):
    shape_r = BoundedNumericProperty(1, min=0.0, max=1.0)
    shape_g = BoundedNumericProperty(0, min=0.0, max=1.0)
    shape_b = BoundedNumericProperty(0, min=0.0, max=1.0)
    shape_a = BoundedNumericProperty(1, min=0.0, max=1.0)
    shape_color = ReferenceListProperty(shape_r, shape_g, shape_b, shape_a)

    def __init__(self, on_close):  # Tools popup menu
        super().__init__('Shape', pos=(200,196))
        self.on_close = on_close
        
        self.popup = ColorPickerPopup(color=self.shape_color, on_color_save=self.on_color_save)
        
        self.button = Button(background_normal='', background_color=self.shape_color, on_press=self.open_color_picker_menu, size=(200,30))
        self.add_widget(self.button)
        
        self.labeled_sliders = {}
        
        labeled_slider = LabeledSlider(text='Density', size=(200,30), min=0, max=5, step=0.05, value=1, to_string=self.slider_string)
        self.add_widget(labeled_slider)
        self.labeled_sliders[labeled_slider.text] = labeled_slider
        
        labeled_slider = LabeledSlider(text='Friction', size=(200,30), min=0, max=2, step=0.02, value=1, to_string=self.slider_string)
        self.add_widget(labeled_slider)
        self.labeled_sliders[labeled_slider.text] = labeled_slider

        labeled_slider = LabeledSlider(text='Elasticity', size=(200,30), min=0, max=2, step=0.02, value=1, to_string=self.slider_string)
        self.add_widget(labeled_slider)
        self.labeled_sliders[labeled_slider.text] = labeled_slider

    def slider_string(self, popup, spinner, text, value):
        command('Shape', text, value)
        return f'{text} = {float(value):.{5}}'

    def open_color_picker_menu(self, instance):
        self.popup.open()
    
    def on_color_save(self, color):
        self.shape_color = color
        self.button.background_color = color
        command('Shape', 'Color', color)

    #def set_option(self, option, value):
        #for labeled_slider in self.labeled_sliders:
            #if labeled_slider.text == option:
                #labeled_slider.slider.value = value
                #self.on_set_option(option, value)
                #return
        #if option == 'Shape color':
            #self.on_color_save(value)
            #return
        #raise UnrecognizedOption(option)
 
