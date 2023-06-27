import random
import requests
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

uid = random.randint(1000, 20000)

API_CHAT_ADDRESS = open('static/server.txt', 'r', encoding='utf-8').read()
chat_addr = API_CHAT_ADDRESS

class ChatApp(App):
    def build(self):
        # Создание главного контейнера
        root_layout = BoxLayout(orientation='vertical')

        # Создание метки для отображения статуса сети
        self.status_label = Label(text='', font_size=12)
        root_layout.add_widget(self.status_label)

        # Создание ScrollView для отображения сообщений чата
        scroll_view = ScrollView()

        # Создание текстового виджета для отображения сообщений чата
        self.chat_text = Label(text='Updating...', font_size=12)
        scroll_view.add_widget(self.chat_text)
        root_layout.add_widget(scroll_view)

        # Создание контейнера для полей ввода и кнопки
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))

        # Создание текстового поля для ввода сообщений
        self.text_input = TextInput()
        input_layout.add_widget(self.text_input)

        # Создание кнопки для отправки сообщений
        send_button = Button(text='Send message')
        send_button.bind(on_press=self.send_story)
        input_layout.add_widget(send_button)

        root_layout.add_widget(input_layout)

        # Запуск функции обновления чата с заданным интервалом
        Clock.schedule_interval(self.update, 1)

        return root_layout

    def frame_update(self, text):
        self.chat_text.text = text

    def check_conn(self):
        try:
            requests.get(chat_addr, verify=False)
            self.status_label.text = '[+] - Network reachable      '
        except:
            self.status_label.text = '[-] - Network unreachable'

    def update(self, *args):
        self.check_conn()
        try:
            chat_text_1 = requests.get(chat_addr + '/allchat', verify=False).text
            chat_text = chat_text_1.replace('\\n', '\n').replace('"', '')
            self.frame_update(chat_text)
        except Exception as e:
            print('\033[91m{}\033[0m'.format(e))

    def send_story(self, *args):
        story = self.text_input.text
        try:
            recv = requests.post(f'{chat_addr}/sendmsg/{uid}/{story}', verify=False).text
            print(recv)
        except:
            print('Error while sending')

if __name__ == '__main__':
    ChatApp().run()
