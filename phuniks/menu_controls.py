from collections import OrderedDict

from .popup_menu_widgets import ImageButton, ImageToggleButton
from .popup_menu import PopupMenu
from .commanding import command, on_command
from .utils import pathto

class ControlsMenu(PopupMenu):
    
    def __init__(self, on_close):  # Tools popup menu

        self.control_dicts = OrderedDict([
            ('Start',       {'source':pathto('images/dvd_start_small.png'),
                                             'toggle':False, 'button':None}),
            ('Rewind',      {'source':pathto('images/dvd_rewind_small.png'),
                                             'toggle':False, 'button':None}),
            ('Pause/Play',  {'source':pathto('images/dvd_play_small.png'),
                                             'toggle':True,  'button':None}),
            ('FastForward', {'source':pathto('images/dvd_fast_forward_small.png'),
                                             'toggle':False, 'button':None}),
            ('End',         {'source':pathto('images/dvd_end_small.png'),
                                             'toggle':False, 'button':None}),
        ])

        super().__init__('Controls', vertical=False, pos=(200,196))
        self.on_close = on_close
        
        for control_name, control_dict in self.control_dicts.items():
            source = control_dict['source']
            if control_dict['toggle']:
                button = ImageToggleButton(source=source, on_press=self.on_press)
            else:
                button = ImageButton(source=source, on_press=self.on_press)
            button.control_name = control_name
            self.add_widget(button)
            control_dict['button'] = button
        on_command('Control', self.activate)

    def activate(self, cmnd, tool_name):
        if tool_name == 'Pause':
            if self.control_dicts['Pause/Play']['button'].state == 'down':
                self.control_dicts['Pause/Play']['button'].trigger_action()
        elif tool_name == 'Play':
            if self.control_dicts['Pause/Play']['button'].state != 'down':
                self.control_dicts['Pause/Play']['button'].trigger_action()
        else:
            self.control_dicts[tool_name]['button'].trigger_action()

    def on_press(self, button):
        if button.control_name == 'Pause/Play':
            if button.state == 'normal':
                button.image.source = pathto('images/dvd_play_small.png')
                command('Pause')
            else:
                button.image.source = pathto('images/dvd_pause_small.png')
                command('Play')
        else:
            command(button.control_name)
