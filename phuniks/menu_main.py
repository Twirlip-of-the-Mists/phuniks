from .popup_menu_widgets import LabeledCheckBox
from .popup_menu import PopupMenu
from .commanding import command, on_command

class MainMenu(PopupMenu):
    
    def __init__(self, sub_menus):  # Tools popup menu
        super().__init__('Phuniks', pos=(200,196), closable=False)
        
        self.buttons = {}
        for menu in sub_menus:
            text=menu.title+'...'
            labeled_checkbox = LabeledCheckBox(text=text, active=False)
            labeled_checkbox.menu = menu
            labeled_checkbox.checkbox.bind(state=self.on_state)
            self.add_widget(labeled_checkbox)
            self.buttons[text] = labeled_checkbox
        on_command('Main', self.activate)
            
    def on_state(self, checkbox, state):
        if state == 'down':
            self.parent.add_widget(checkbox.parent.menu)
        else:
            self.parent.remove_widget(checkbox.parent.menu)

    def activate(self, cmnd, menu_name):
        self.buttons[menu_name].trigger_action()
