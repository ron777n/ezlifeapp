import requests
from database import DataBase
import json
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

#Window.size = (370, 810)

class Create(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password.text != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.login()

            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.namee.text = ""
        self.password.text = ""

class MainWin(Screen):
    welcome = ObjectProperty(None)

    def LogOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        self.databass = db.get_user(self.current)
        password = self.databass["password"]
        name = self.databass["name"]
        created = self.databass["created"]
        self.welcome.text = "welcome: " + name
        self.has_sidebar = False

    def menu(self):
        if not self.has_sidebar:
            print('adding sidebar')
            self.side = SideBar()
            self.add_widget(self.side)
            self.has_sidebar = True
        else:
            print('removing sidebar')
            self.remove_widget(self.side)
            self.has_sidebar = False

class Library(Screen):
    pass

class SideBar(BoxLayout):
    def library(self):
        sm.current = "Library"

class LoginWin(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    def loginBtn(self):
        if db.validate(self.email.text.strip().replace(".", "-"), self.password.text):
            MainWin.current = self.email.text.strip().replace(".", "-")
            self.reset()
            sm.current = "MainWin"
        else:
            invalidLogin()

    def reset(self):
        self.email.text = ""
        self.password.text = ""

    def login(self):
        sm.current = "create"

class WinManager(ScreenManager):
    pass


kv = Builder.load_file("main.txt")

sm = WinManager()

screens = [LoginWin(name="login"), MainWin(name="MainWin"), Create(name="create"), Library(name="Library")]
for screen in screens:
    sm.add_widget(screen)

class EZlifeApp(App):
    def build(self): #todo add logo's to each of the other apps
        return sm
    def on_start(self):
        data()

def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=kivy.uix.label.Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

def data():
    global db
    db = DataBase("https://ezapp-3e11d-default-rtdb.firebaseio.com", "IL0pb9MSHelIUVnVLoHHKm4tyckCbEZLNSzzQ477")

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=kivy.uix.label.Label(text='Invalid email or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

db = ""

if __name__ == "__main__":
    EZlifeApp().run()