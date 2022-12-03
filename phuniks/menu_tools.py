from collections import OrderedDict

from kivy.uix.togglebutton import ToggleButton

from .popup_menu import PopupMenu
from .commanding import command, on_command

class ToolsMenu(PopupMenu):
    
    def __init__(self, on_close):  # Tools popup menu
        super().__init__('Tools', pos=(200,196))

        tool_names = [
            ('Brush', 'Make'),
            ('Circle', 'Make'),
            ('Rectangle', 'Make'),
            #('Polygon', 'Make'),
            ('Plane', 'Make'),
            #('Attach', 'Join'),
            #('Hinge', 'Join'),
            #('Spring', 'Join'),
            #('Grab', 'Modify'),
            #('Select', 'Modify'),
            ('Kill', 'Modify'),
            ('Explode', 'Modify')
        ]
        self.on_close = on_close
        
        self.tools = {}
        for tool_name, tool_type in tool_names:
            button = ToggleButton(text=tool_name, group='tools')
            button.tool_type = tool_type
            button.texture_update()
            button.size = (button.texture_size[0] + 10, button.texture_size[1] + 10)
            button.bind(state=self.on_state)
            self.add_widget(button)
            self.tools[tool_name] = button
     
        on_command('Tool', self.activate)
        self.current = self.tools['Brush']
        command('Tool', self.current.text)
     
    def activate(self, cmnd, tool_name):
        if self.tools[tool_name].state != 'down':
            for button in self.tools.values():
                button.state = 'normal'
            self.tools[tool_name].state = 'down'
    
    def on_state(self, instance, state):
        if state == 'down':
            if self.current is not instance:
                command(instance.tool_type, instance.text)
                self.current = instance

    def on_touch_down(self, touch):
        result = super().on_touch_down(touch)
        if self.current.state != 'down':
            self.current.state = 'down'
        return result
