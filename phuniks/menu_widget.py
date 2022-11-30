#from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

from .menu_tools import ToolsMenu
from .menu_controls import ControlsMenu
from .menu_options import OptionsMenu
from .menu_view import ViewMenu
from .menu_shape import ShapeMenu
from .menu_main import MainMenu
from .commanding import command


class MenuWidget(FloatLayout):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rmb_popup = None
        
        self.tools_menu = ToolsMenu(self.popup_menu_close)
        self.controls_menu = ControlsMenu(self.popup_menu_close)
        self.view_menu = ViewMenu(self.popup_menu_close)
        self.options_menu = OptionsMenu(self.popup_menu_close)
        self.shape_menu = ShapeMenu(self.popup_menu_close)

        self.sub_menus = [self.tools_menu, self.controls_menu, self.view_menu, self.options_menu, self.shape_menu]

        self.main_menu = MainMenu(self.sub_menus)
        
        self.all_menus = self.sub_menus + [self.main_menu]
        
        ## File selector popup menu
        #self.fileopen_popup = PopupMenu('Open File', pos=(200,196))
        #self.fileopen_popup.on_close = self.popup_menu_close
        #fclv = FileChooserListView(size=Vector(self.size)/2)
        #self.fileopen_popup.add_widget(fclv)

        space = 5
        self.main_menu.pos = (space, self.height - self.main_menu.height - space)

        self.tools_menu.pos = (space, self.height - self.main_menu.height - self.tools_menu.height - 2*space)

        self.view_menu.pos = (2*space + self.main_menu.width, self.height - self.view_menu.height - space)

        self.controls_menu.pos = (self.view_menu.x + self.view_menu.width + space, self.height - self.controls_menu.height - space)

        self.options_menu.pos = (self.controls_menu.x + self.controls_menu.width + space, self.height - self.options_menu.height - space)
        
        self.shape_menu.pos = (self.width - self.shape_menu.width - space, self.height - self.shape_menu.height - space)
        
        self.add_widget(self.main_menu)
        command('Main', 'Tools...')
        command('Main', 'View...')
        command('Main', 'Controls...')
        
    def popup_menu_close(self, instance, value):
        command('Main', instance.title + '...')
        
