import requests
from database import *
import json
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

Window.size = (370, 810)


class Create(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password.text != "":
                users.add_user(self.email.text, self.password.text, self.namee.text)

                self.login()

            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "Login"

    def reset(self):
        self.email.text = ""
        self.namee.text = ""
        self.password.text = ""


class MainWin(Screen):
    welcome = ObjectProperty(None)
    last_pages = ObjectProperty(None)

    def __init__(self, name):
        super().__init__()
        self.side = SideBar()
        self.has_sidebar = False

    def LogOut(self):
        sm.current = "Login"

    def on_enter(self, *args):
        self.side.current = self.current
        self.users = users.get_user(self.current)
        name = self.users["name"]
        self.welcome.text = "welcome: " + name
        self.builder()

    def menu(self):
        if not self.has_sidebar:
            print('adding sidebar')
            self.add_widget(self.side)
            self.has_sidebar = True
        else:
            print('removing sidebar')
            self.remove_widget(self.side)
            self.has_sidebar = False

    def on_leave(self):
        self.last_pages.clear_widgets()
        self.remove_widget(self.side)
        self.has_sidebar = False

    def builder(self):
        if "last_pages" in self.users:
            for element in self.users["last_pages"]:
                Button_el = kivy.uix.button.Button(text=element)
                setattr(Button_el, "on_release", self.tot(element))
                self.last_pages.add_widget(Button_el)
        else:
            print("not found")

    def tot(self, page):
        return lambda: self.tut(page)

    def tut(self, page):
        print(page)
        Library.current = self.current
        Library.tutorial(page, self.current)


class Tutorial_page(Screen):
    def on_enter(self):
        self.builder(self.current)

    def builder(self, additions, *args):
        for instance in additions:
            for attribute in additions[instance]:
                if (attribute == "size_hint" or attribute == "pos_hint"):
                    self.layout = kivy.uix.floatlayout.FloatLayout()
                    break
                else:
                    self.layout = BoxLayout(orientation="vertical")
            else:
                continue
            break
        self.add_widget(self.layout)

        for instance in additions:
            if "text" in instance:
                label = kivy.uix.label.Label()
                for attribute in additions[instance]:
                    setattr(label, attribute, additions[instance][attribute])

                self.layout.add_widget(label)
            if "button" in instance:
                Button = kivy.uix.button.Button()
                for attribute in additions[instance]:
                    if attribute in ("on_release", "on_click"):
                        try:
                            at_got = getattr(self, additions[instance][attribute])
                            setattr(Button, attribute, at_got)
                        except AttributeError:
                            try:
                                nf = additions[instance][attribute]
                                functions = {}
                                exec(nf, functions)
                                setattr(Button, attribute, functions["main"])
                            except Exception as e:
                                print(e)
                        finally:
                            continue
                    setattr(Button, attribute, additions[instance][attribute])

                self.layout.add_widget(Button)
            if "input" in instance:
                textinput = kivy.uix.textinput.TextInput()
                for attribute in self.current[instance]:
                    setattr(textinput, attribute, self.current[instance][attribute])
                self.layout.add_widget(textinput)

    def on_leave(self):
        self.clear_widgets()

    def back(self):
        sm.current = "Library"


class Library(Screen):
    def main(self):
        sm.current = "MainWin"

    def up_tut(self, page):
        Library.tutorial(page, self.current)

    @staticmethod
    def tutorial(page, current):
        Library.adl(page, current)
        Tutorial_page.current = tutorials.get_tutorial(page)
        sm.current = "Tutorials"  # tutorials.get_tutorial(page))

    @staticmethod
    def adl(tutorial, current):
        var_user = users.get_user(current)
        last_pages_list = var_user["last_pages"]
        if "last_pages" in var_user:
            if tutorial not in last_pages_list:
                last_pages_list.insert(0, tutorial)
            else:
                last_pages_list.insert(0, last_pages_list.pop(last_pages_list.index(tutorial)))
            if len(last_pages_list) > 4:
                last_pages_list.pop()
        else:
            last_pages_list = [tutorial]
        users.get_user(current)["last_pages"] = last_pages_list


class SideBar(BoxLayout):
    def library(self):
        Library.current = self.current
        sm.current = "Library"


class LoginWin(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if users.validate(self.email.text.strip().replace(".", "-"), self.password.text):
            MainWin.current = self.email.text.strip().replace(".", "-")
            self.reset()
            sm.current = "MainWin"
        else:
            invalidLogin()

    def reset(self):
        self.email.text = ""
        self.password.text = ""

    def login(self):
        sm.current = "Create"


class WinManager(ScreenManager):
    pass


kv = Builder.load_file("main.kv")

sm = WinManager()

screens = [LoginWin(name="Login"), MainWin(name="MainWin"), Create(name="Create"), Library(name="Library"),
           Tutorial_page(name="Tutorials")]
for screen in screens:
    sm.add_widget(screen)


class EZlifeApp(App):
    def build(self):  # todo add logo's to each of the other apps
        return sm

    def on_start(self):
        data()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=kivy.uix.label.Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


def data():
    global users, tutorials
    users = Users("https://ezapp-3e11d-default-rtdb.firebaseio.com", "IL0pb9MSHelIUVnVLoHHKm4tyckCbEZLNSzzQ477")
    tutorials = Tutorials("tutorials.json")


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=kivy.uix.label.Label(text='Invalid email or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


if __name__ == "__main__":
    EZlifeApp().run()

users.save()
