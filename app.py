from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
import json
import os

class AppStyle():
    def __init__(self):
        self.bg_color0 = (17, 18, 23)
        self.bg_color1 = (22, 23, 28)
        self.bg_color2 = (37, 38, 43)
        self.main_font = self._create_font()
        self.main_font_bold = self._create_font()
        self.main_font_bold.setBold(True)
        self.white = (200, 200, 200)
        self.whiteQColor = QtGui.QColor(self.white[0], self.white[1], self.white[2])

        self.menu_buttons_alignment = Qt.AlignmentFlag.AlignLeft

        self.dark_color_contact = (37, 39, 48)
        self.light_color_contact = (44, 46, 56)

        self.button_size = 150
        self.button_style = f'background-color: rgb{self.white}; border-radius: 10px; padding: 7px; margin-right: 15px;'

        self.input_style = f'background-color: rgb{self.white}; border-radius: 10px; padding: 7px; margin-bottom: 15px;'

    def _create_font(self):
        font = QtGui.QFont("Times", 12)
        font.setFamily("Times")
        font.setPointSize(13)
        return font


class App(QtWidgets.QApplication):
    def __init__(self):
        super().__init__()
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("AutoZap")
        self.window.resize(1000, 600)
        self.app_style = AppStyle()
        self.window.setStyleSheet(f"background-color: rgb{self.app_style.bg_color0};")
        self.contacts_data = self._load_contacts_data()
        self._create_layout()
        self._basic_ui_widgets()
        self._update_contacts()
        self._updateMessages()
        self._create_add_contact_window()
        self.window.setLayout(self.main_layout)
        self.window.show()
        self.exec()

    def _load_contacts_data(self):
        if os.path.exists("contacts_data.json"):
            with open("contacts_data.json", "r") as file:
                return json.load(file)
        else:
            return []

    def _save_contacts_data(self):
        with open("contacts_data.json", "w") as file:
            json.dump(self.contacts_data, file)

    def _create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.menu_layout = QtWidgets.QHBoxLayout()
        self.menu_layout.setAlignment(self.app_style.menu_buttons_alignment)
        self.main_layout.addLayout(self.menu_layout)

        self.operation_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.operation_layout)

        self.contacts = QtWidgets.QListWidget()
        self.messages = QtWidgets.QListWidget()
        self.contacts.setStyleSheet(f"background-color: rgb{self.app_style.bg_color1};")
        self.messages.setStyleSheet(f"background-color: rgb{self.app_style.bg_color1};")
        self.operation_layout.addWidget(self.contacts)
        self.operation_layout.addWidget(self.messages)

    def _basic_ui_widgets(self):
        tam_button = self.app_style.button_size 
        self.add_contact_button = QtWidgets.QPushButton("Add Contact")
        self.add_contact_button.clicked.connect(self.add_contact)
        self.menu_layout.addWidget(self.add_contact_button)
        self.add_contact_button.setStyleSheet(self.app_style.button_style)
        self.add_contact_button.setFont(self.app_style.main_font)
        self.add_contact_button.setFixedWidth(tam_button)

        self.delete_contact_button = QtWidgets.QPushButton("Delete Contact")
        self.delete_contact_button.clicked.connect(self.deleteContact)
        self.menu_layout.addWidget(self.delete_contact_button)
        self.delete_contact_button.setStyleSheet(self.app_style.button_style)
        self.delete_contact_button.setFont(self.app_style.main_font)
        self.delete_contact_button.setFixedWidth(tam_button)

        self.message_layout = QtWidgets.QVBoxLayout()
        self.operation_layout.addLayout(self.message_layout)

    def _update_contacts(self):
        self.contacts.clear()
        colors = [self.app_style.dark_color_contact, self.app_style.light_color_contact]
        for idx, contact in enumerate(self.contacts_data):
            item = QtWidgets.QListWidgetItem(contact["name"] + " - " + contact["number"])
            c = colors[idx % 2]
            item.setFont(self.app_style.main_font_bold)
            item.setForeground(self.app_style.whiteQColor)
            item.setBackground(QtGui.QColor(c[0], c[1], c[2]))
            self.contacts.addItem(item)

    def _updateMessages(self):
        pass

    def _create_add_contact_window(self):
        self.add_contact_window = QtWidgets.QWidget()
        self.add_contact_window.setWindowTitle("Add Contact")
        self.add_contact_window.resize(300, 100)
        self.add_contact_window.setLayout(QtWidgets.QVBoxLayout())
        self.add_contact_window.setStyleSheet(f"background-color: rgb{self.app_style.bg_color2};")

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet(self.app_style.input_style)
        self.add_contact_window.layout().addWidget(self.name_input)

        self.number_input = QtWidgets.QLineEdit()
        self.number_input.setPlaceholderText("Number")
        self.number_input.setStyleSheet(self.app_style.input_style)
        self.add_contact_window.layout().addWidget(self.number_input)

        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_contact)
        self.submit_button.setStyleSheet(self.app_style.button_style)
        self.add_contact_window.layout().addWidget(self.submit_button)

        self.number_input.returnPressed.connect(self.submit_contact)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        keys = QtCore.Qt.Key
        match key:
            case keys.Key_Escape:
                self.add_contact_window.close()
                return

    def add_contact(self):
        self.name_input.setText("")
        self.number_input.setText("")
        self.add_contact_window.show()

    def deleteContact(self):
        row = self.contacts.currentRow()
        if row >= 0:
            del self.contacts_data[row]
            self._save_contacts_data()
            self._update_contacts()

    def submit_contact(self):
        name = self.name_input.text()
        number = self.number_input.text()
        self.contacts_data.append({
            "name": name,
            "number": number
        })
        self._save_contacts_data()
        self._update_contacts()
        self.add_contact_window.close()

app = App()
