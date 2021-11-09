from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
import sqlite3
import socket
import threading

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        screen = Builder.load_file('style.kv')
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists users(username ,password,email)""")
        return screen


    def register(self):
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        sql_command = "INSERT INTO users (username , email, password) VALUES (?, ?, ?)"
        values = (self.root.ids.user.text, self.root.ids.email.text, self.root.ids.password.text)
        if self.root.ids.user.text != '' and self.root.ids.email.text != '' and self.root.ids.password.text != '':
            c.execute(sql_command, values)
            conn.commit()
            self.root.ids.user.text = ""
            self.root.ids.password.text = ""
            self.root.ids.email.text = ""
            self.dialog = MDDialog(
                title="Register successfully",
                radius=[20, 7, 20, 7],
            )
            self.dialog.open()
        else:
            self.dialog = MDDialog(
                title="Error:",
                text="You need to fill all fields!!",
                radius=[20, 7, 20, 7],
            )
            self.dialog.open()

    def login(self):
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (self.root.ids.user1.text, self.root.ids.password1.text))
        conn.commit()
        if c.fetchall():
            self.root.current = 'screen2'

        else:
                self.dialog = MDDialog(
                    title="Error:",
                    text = "Something is wrong, check username and password!!",
                    radius=[20, 7, 20, 7],
                )
                self.dialog.open()

    def sent_message(self):
        client.send((f"{self.root.ids.chat_nick.text}: {self.root.ids.chat_text.text}".encode('utf-8')))
        self.root.ids.chat_text.text = ""


    def connect_to_server(self):
        if self.root.ids.chat_nick.text != "":
            client.connect((self.root.ids.IP_address.text,666))
            message = client.recv(1024).decode('utf-8')
            if message == "Nick":
                client.send(self.root.ids.chat_nick.text.encode('utf-8'))
                self.root.ids.connection_btn.disabled = True
                self.root.ids.chat_text.disabled = False
                self.root.ids.send_text_btn.disabled = False
                self.root.ids.IP_address.disabled = True
                self.root.ids.chat_nick.disabled = True
                thread = threading.Thread(target=self.recive)
                thread.start()
    def recive(self):
        stop = False
        while not stop:
            try:
                message = client.recv(1024).decode('utf-8')
                self.root.ids.chat_history.text += message + "\n"
            except:
                client.close()
                stop = True


MainApp().run()