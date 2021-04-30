import datetime
import requests
import json
import time

class DataBase:
    def __init__(self, url="https://ezapp-3e11d-default-rtdb.firebaseio.com", auth="IL0pb9MSHelIUVnVLoHHKm4tyckCbEZLNSzzQ477"):
        self.users = None
        self.url = url
        self.auth = auth

        databass = ''
        while databass == '':
            try:
                self.databass = requests.get(self.url + "/users/.json" + "?auth=" + self.auth).json()
                break
            except:
                print("Connection refused by the server..")
                print("waiting for 2 and a half seconds")
                time.sleep(2.5)
                print("retrying")
                continue

        print(self.databass)
        self.load()

    def load(self):
        self.users = {}



        for user in self.databass:
            password = self.databass[user]["password"]
            name = self.databass[user]["name"]
            created = self.databass[user]["created"]
            self.users[user] = {"password": password, "name" : name, "created" : created}

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip().replace(".", "-")] = {"password" : password.strip(), "name" : name.strip(), "created" : DataBase.get_date()}
            self.save()
            return 1
        else:
            print("Email exists already")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email]["password"] == password
        else:
            return False

    def save(self):
        #print("users: " + str(type(self.users)) + str(self.users))
        print(requests.patch(url= self.url + "/users/.json", json = self.users))

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]


