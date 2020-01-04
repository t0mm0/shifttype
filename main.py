from kivymd.app import MDApp
from kivy.config import Config

Config.read('config.ini')


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "shiftTYPE"
        super().__init__(**kwargs)
    pass


if __name__ == '__main__':
    app = MainApp()
    app.run()
