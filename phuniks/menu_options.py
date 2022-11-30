from .popup_menu_widgets import LabeledCheckBox, LabeledSlider
from .popup_menu import PopupMenu
from .commanding import command, on_command

class OptionsMenu(PopupMenu):
    
    true_values = ['t', 'true', 'on']
    false_values = ['f', 'false', 'off']
    change_values = ['c', 'change', 'toggle', 's', 'swap']

    def __init__(self, on_close):  # Tools popup menu
        super().__init__('Options', pos=(200,196))
        self.on_close = on_close

        self.labeled_checkboxs = {}
        for text in ['Gravity', 'Air resistance', 'Draw edges', 'Draw joins']:
            name = text.title().replace(' ', '')
            labeled_checkbox = LabeledCheckBox(text=text, active=True)
            labeled_checkbox.checkbox.bind(state=self.on_state)
            labeled_checkbox.checkbox.cmnd_name = name
            
            self.add_widget(labeled_checkbox)
            self.labeled_checkboxs[name] = labeled_checkbox
            self.on_state(labeled_checkbox.checkbox, 'down')

        self.speed_slider = LabeledSlider(text='Speed', size=(200,30), min=0.1, max=4, step=0.1, value=1.0, to_string=self.speed_string)
        self.add_widget(self.speed_slider)

        on_command('Option', self.on_command)
        
    def on_state(self, instance, state):
        command(instance.cmnd_name, 'True' if state=='down' else 'False')

    def on_command(self, cmnd, subcmnd, value):
        if subcmnd in self.labeled_checkboxs:
            cb = self.labeled_checkboxs[subcmnd].checkbox
            if value.lower() in self.true_values:
                cb.state = 'down'
            elif value.lower() in self.true_values:
                cb.state = 'normal'
            elif value.lower() in self.change_values:
                if cb.state == 'down':
                    cb.state = 'normal'
                else:
                    cb.state = 'down'
    
    def speed_string(self, popup, spinner, text, value):
        command('Speed', value)
        return f'{text} = {float(value):.{5}}x'
